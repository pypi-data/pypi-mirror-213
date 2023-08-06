"""
Tools related to raster operations:

- Reproject a raster to a new geographic coordinate system
"""

__all__ = ["reproject", "resample", "to_mapbox"]

import tqdm, os, pathlib, warnings, requests, shutil, subprocess, json, time


def reproject(filepath: str, save_path: str = None, new_crs: int = 3857) -> None:
    """Reproject a GeoTiff file.

    Reproject a GeoTiff file to a new geographic coordinate system.
    
    Args:
        filepath: Filepath of where the raster is stored.
        save_path: Filepath of where the reprojected raster is to be saved. If None, then the original filepath is used and the data is overwritten.
        new_crs: The (typically 4 digit) EPSG code to reproject the GeoTiff to.
    
    Returns:
        None.
    """
   
    try:
        import rasterio as rio
        from rasterio import warp as rio_warp
    except ModuleNotFoundError:
        raise ModuleNotFoundError("RasterIO could not be located. Please install RasterIO seperately into this Python environment, or run 'pip install uintel[full]'")
    
    new_crs = f'EPSG:{new_crs}'
    
    with rio.open(filepath) as raster:
        # Grab all the data and metadata
        data = raster.read()
        profile = raster.profile.copy()
        old_transform, old_crs = raster.transform, raster.crs
        # Determine the new transform, width and height of the new raster
        transform, width, height = rio_warp.calculate_default_transform(raster.crs, new_crs, raster.width, raster.height, *raster.bounds)

    # Update the profile with the new values
    profile.update({
        'crs': new_crs,
        'transform': transform,
        'width': width,
        'height': height,
        "compress": "deflate",
        "zlevel": 9,
        "predictor": 2,
    })

    if not save_path:
        # Replace in place
        save_path = filepath
    os.makedirs(pathlib.Path(save_path).parent, exist_ok=True)

    with rio.open(filepath, 'w', **profile) as dst:
        # Reproject each band seperately
        for band_number in tqdm.tqdm(range(profile["count"]), f"Reprojecting {filepath} to {new_crs}", total=profile["count"], leave=False, dynamic_ncols=True):
            _ = rio_warp.reproject(
                source=data[band_number],
                destination=rio.band(dst, band_number+1),
                src_transform=old_transform,
                src_crs=old_crs,
                dst_transform=transform,
                dst_crs=new_crs)


def resample(filepath: str, save_path: str = None, upscale_factor: float = 0.5, resampling: str = "nearest") -> None:
    """Resample a GeoTiff file.

    Resample a GeoTiff file by an upscaling factor.
    
    Args:
        filepath: Filepath of where the raster is stored.
        save_path: Filepath of where the resampled raster is to be saved. If None, then the original filepath is used and the data is overwritten.
        upscale_factor: If the upscale factor is greater than 1, the raster is upsampled and pixel sizes are made smaller. Conversly, if the upscale factor is less than 1 and greater then zero, the raster is downsampled and pixel sizes are made bigger.
        resampling: The resampling method to use. For available methods, please see https://rasterio.readthedocs.io/en/stable/topics/resampling.html#resampling-methods
    
    Returns:
        None.
    """
   
    try:
        import rasterio as rio
        from rasterio.enums import Resampling
    except ModuleNotFoundError:
        raise ModuleNotFoundError("RasterIO could not be located. Please install RasterIO seperately into this Python environment, or run 'pip install uintel[full]'")

    if upscale_factor == 1:
        # No upscaling factor given
        warnings.warn(f"Resampling {filepath} was skipped due to an upscaling factor of 1")
        return
    elif upscale_factor <= 0:
        # Bad upscaling factor given
        warnings.warn(f"Resampling {filepath} was skipped due to an upscaling factor of {upscale_factor}")
        return

    with rio.open(filepath, "r") as hazard:
        # Resample the hazard into a larger tile size to reduce file size
        hazard_array = hazard.read(
            out_shape=(hazard.count, int(hazard.height * upscale_factor), int(hazard.width * upscale_factor)),
            resampling=getattr(Resampling, resampling)
        )
        transform = hazard.transform * hazard.transform.scale((hazard.width / hazard_array.shape[-1]),(hazard.height / hazard_array.shape[-2]))  
        # Set metadata
        output_meta = hazard.meta.copy()
    
    # Update the profile with the new values
    output_meta.update({
        "height": hazard_array.shape[1],
        "width": hazard_array.shape[2],
        "transform": transform,
        "compress": "deflate",
        "predictor": 2,
        "zlevel": 9
    })

    if not save_path:
        # Replace in place
        save_path = filepath
    os.makedirs(pathlib.Path(save_path).parent, exist_ok=True)
   
    with rio.open(save_path, 'w', **output_meta) as destination:
        destination.write(hazard_array)


def to_mapbox(filepath: str, tileset_id: str, token: str, display_name: str = None, show_progress: bool = False) -> None:
    """Upload a GeoTiff to MapBox as a tileset layer.
    
    Upload a GeoTiff to MapBox as a tileset layer, with the given tileset ID and (optional) display name. Based upon https://docs.mapbox.com/api/maps/uploads/
    
    Args:
        filepath: Filepath of where the raster is stored.
        tileset_id: The tileset ID to create or replace, in the format username.nameoftileset. Limited to 32 characters which does not include the username. The only allowed special characters are - and _. 
        token: A valid access token for MapBox, with at least the following scopes: uploads:write, uploads:read
        display_name: The name of the tileset shown on the MapBox Studio Web UI. Limited to 64 characters.
        show_progress: If True, a progress bar will be shown during the conversion procedure. 
    
    Returns:
        None.
    """
    
    mapbox_username = tileset_id.split(".")[0]

    # Step 1a - Get the AWS S3 credentials to upload the file
    response = requests.post(f"https://api.mapbox.com/uploads/v1/{mapbox_username}/credentials?access_token={token}")
    if response.ok:
        aws_credentials = response.json()
    else:
        raise RuntimeError("Authentication failed with MapBox. Please check the API key is valid and has the right scopes.")

    # Step 1b - Write the temporary credentials to file
    aws_credentials_save_path = os.path.expanduser("~/.aws/credentials")
    if os.path.exists(aws_credentials_save_path):
        # Keep a copy in case the user has their credentials
        _ = shutil.move(aws_credentials_save_path, aws_credentials_save_path+"_old")
    with open(aws_credentials_save_path, "w") as credentials_file:
        _ = credentials_file.write(f"[default]\naws_access_key_id = {aws_credentials['accessKeyId']}\naws_secret_access_key = {aws_credentials['secretAccessKey']}\naws_session_token = {aws_credentials['sessionToken']}\n")

    
    # Step 2 - Upload the tiff to the S3 bucket
    response = subprocess.run([f"aws s3 cp '{filepath}' s3://{aws_credentials['bucket']}/{aws_credentials['key']} --region us-east-1"], capture_output=True, shell=True)
    if response.returncode != 0:
        raise RuntimeError(f"Uploading {filepath} to the AWS S3 staging bucket failed due to:\n{response.stderr.decode()}")


    # Step 3 - Begin the upload process to Mapbox Uploads API
    data = {
        "url": f"http://{aws_credentials['bucket']}.s3.amazonaws.com/{aws_credentials['key']}", 
        "tileset": tileset_id, 
        "name": display_name
    }
    command = f"""curl -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{json.dumps(data)}' 'https://api.mapbox.com/uploads/v1/{mapbox_username}?access_token={token}'"""
    response = subprocess.run([command], shell=True, capture_output=True)
    if response.returncode != 0:
        raise RuntimeError(f"Converting {filepath} to a tileset failed:\n{response.stderr.decode()}")
    if "Invalid" in response.stdout.decode():
        raise RuntimeError(f"Converting {filepath} to a tileset failed because:\n{response.stdout.decode()}")
    
    # Step 4 - Track the progress of the conversion if the user wants it displayed
    if not show_progress:
        upload_id = json.loads(response.stdout.decode())["id"]
        progress = json.loads(response.stdout.decode())["progress"]
        progress_bar = tqdm(desc=f"Converting {pathlib.Path(filepath).name} to tileset", total=1, leave=True, dynamic_ncols=True)
        while progress < 1:
            response = subprocess.run([f'curl "https://api.mapbox.com/uploads/v1/{mapbox_username}/{upload_id}?access_token={token}"'], shell=True, capture_output=True)
            if response.returncode == 0:
                progress = json.loads(response.stdout.decode())["progress"]
                progress_bar.n = progress
                _ = progress_bar.refresh()
                time.sleep(1)
            else:
                raise RuntimeError(f"An error occured fetching the progress of the conversion. It should still be running in the background, so please manually check at https://studio.mapbox.com/tilesets/. See below:\n{response.reason}")

    # Step 4 - Delete temporary credentials
    if os.path.exists(aws_credentials_save_path+"_old"):
        _ = shutil.move(aws_credentials_save_path+"_old", aws_credentials_save_path)
    else:
        os.remove(aws_credentials_save_path)

