from collections import defaultdict

from saleor.graphql.core.dataloaders import DataLoader

from saleor.vendors.models import VendorImage


class ImagesByVendorIdLoader(DataLoader):
    context_key = "images_by_vendor"

    def batch_load(self, keys):
        images = VendorImage.objects.filter(vendor_id__in=keys)
        image_map = defaultdict(list)
        for image in images:
            image_map[image.vendor_id].append(image)
        return [image_map[vendor_id] for vendor_id in keys]
