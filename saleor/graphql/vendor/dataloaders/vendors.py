from collections import defaultdict

from saleor.graphql.core.dataloaders import DataLoader

from saleor.vendors.models import VendorServiceImage, VendorMainImage


class ServiceImagesByVendorIdLoader(DataLoader):
    context_key = "service_images_by_vendor"

    def batch_load(self, keys, last=5):
        images = VendorServiceImage.objects.filter(vendor_id__in=keys)[:last]
        image_map = defaultdict(list)
        for image in images:
            image_map[image.vendor_id].append(image)
        return [image_map[vendor_id] for vendor_id in keys]

# class PastExperiencesByVendorIdLoader(DataLoader):
#     context_key = "past_experiences_by_vendor"

#     def batch_load(self, keys)


# class MainImagesByVendorIdLoader(DataLoader):
#     context_key = "main_images_by_vendor"

#     def batch_load(self, keys, last=5):
#         images = VendorMainImage.objects.filter(vendor_id__in=keys)[:last]
#         image_map = defaultdict(list)
#         for image in images:
#             image_map[image.vendor_id].append(image)
#         return [image_map[vendor_id] for vendor_id in keys]
