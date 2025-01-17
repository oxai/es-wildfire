## Initial Setup for Sentinelhub

To use Sentinel Hub, run ```pip install sentinelhub``` (if you are a Windows user first install [shapely](https://www.lfd.uci.edu/~gohlke/pythonlibs/))

Create an account for Sentinel Hub at https://www.sentinel-hub.com/ and create an instance following https://sentinelhub-py.readthedocs.io/en/latest/.
Set your instance id by running ```sentinelhub.config --instance_id <instance_id>```. If you are looking at Landsat instead of Sentinel, you may also have to modify the OGC endpoint from https://services.sentinel-hub.com/ogc/ to https://services-uswest2.sentinel-hub.com/ogc/.

There are two options for using Sentinel - one is using WMS and the other is using WCS. WCS gives the pixel resolution regardless of image size so this is what we want to use.

