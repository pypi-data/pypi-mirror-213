from enum import Enum

class ViewId(Enum):
    """
    Enum for representing Google Picker View IDs.

    Each attribute represents a different view that can be used in the Google Picker. 
    For more information about what these views mean, check the Google Picker API documentation:
    https://developers.google.com/drive/picker/reference?#view-id
    """
    DOCS = "all"
    DOCS_IMAGES = "docs-images"
    DOCS_IMAGES_AND_VIDEOS = "docs-images-and-videos"
    DOCS_VIDEOS = "docs-videos"
    DOCUMENTS = "documents"
    DRAWINGS = "drawings"
    FOLDERS = "folders"
    FORMS = "forms"
    IMAGE_SEARCH = "image-search"
    MAPS = "maps"
    PDFS = "pdfs"
    PHOTOS = "photos"
    PHOTO_ALBUMS = "photo-albums"
    PHOTO_UPLOAD = "photo-upload"
    PRESENTATIONS = "presentations"
    RECENTLY_PICKED = "recently-picked"
    SPREADSHEETS = "spreadsheets"
    VIDEO_SEARCH = "video-search"
    WEBCAM = "webcam"
    YOUTUBE = "youtube"

class Feature(Enum):
    """
    Enum for representing Google Picker Features.

    Each attribute represents a different feature that can be used in the Google Picker. 
    For more information about what these features mean, check the Google Picker API documentation:
    https://developers.google.com/drive/picker/reference?#feature
    """
    Cba = "shadeDialog"
    E9 = "ftd"
    Hba = "simpleUploadEnabled"
    I8 = "cropA11y"
    Jca = "urlInputVisible"
    K9 = "formsEnabled"
    MINE_ONLY = "mineOnly"
    MULTISELECT_ENABLED = "multiselectEnabled"
    NAV_HIDDEN = "navHidden"
    SIMPLE_UPLOAD_ENABLED = "simpleUploadEnabled"
    SUPPORT_DRIVES = "sdr"
    SUPPORT_TEAM_DRIVES = "std"
    T_DOLLAR = "mineOnly"
    U_DOLLAR = "minimal"
    Uaa = "profilePhoto"
    V_DOLLAR = "minew"
    A_DOLLAR = "horizNav"
    bca = "sawffmi"
    daa = "multiselectEnabled"
    G_DOLLAR = "ignoreLimits"
    iaa = "navHidden"
    kaa = "newDriveView"
    laa = "newHorizNav"
    m9 = "showAttach"
    maa = "newPhotoGridView"
    n9 = "edbe"
    oca = "sdr"
    qca = "std"
    waa = "odv"