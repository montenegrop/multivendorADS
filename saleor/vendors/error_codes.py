from enum import Enum


class VendorErrorCode(Enum):
    ALREADY_EXISTS = "already_exists"
    DUPLICATED_INPUT_ITEM = "duplicated_input_item"
    GRAPHQL_ERROR = "graphql_error"
    INVALID = "invalid"
    NOT_VENDOR_MAIN_IMAGE = "not_vendor_main_image"
    NOT_VENDOR_IMAGES = "not_vendor_images"
    NOT_FOUND = "not_found"
    REQUIRED = "required"
    UNIQUE = "unique"
