import os
from datetime import datetime
from enum import Enum
from typing import List, Optional
from urllib.parse import urljoin, urlparse

from pydantic import BaseModel, HttpUrl

from bpkio_api.models.common import BaseResource, NamedModel, PropertyMixin
from bpkio_api.models.Sources import (
    AdServerSource,
    SlateSource,
    SourceFormat,
    SourceSparse,
)
from bpkio_api.models.TranscodingProfiles import (
    TranscodingProfile,
    TranscodingProfileId,
)


class ServiceType(Enum):
    AD_INSERTION = "ad-insertion"
    VIRTUAL_CHANNEL = "virtual-channel"
    CONTENT_REPLACEMENT = "content-replacement"

    def __str__(self):
        return str(self.value)


# === SERVICES Models ===


class ServiceIn(NamedModel, PropertyMixin):
    environmentTags: Optional[List[str]] = []


class WithCommonServiceFields(BaseResource):
    url: HttpUrl
    creationDate: datetime
    updateDate: datetime

    @property
    def serviceId(self):
        return self.url.path.split("/")[1]

    @property
    def full_url(self):
        return self.make_full_url()

    def make_full_url(self, *args, **kwargs):
        return self.url

    @property
    def format(self):
        ext = os.path.splitext(urlparse(self.url).path)[1]
        match ext:
            case ".m3u8":
                return SourceFormat.HLS
            case ".mpd":
                return SourceFormat.DASH


class ServiceSparse(ServiceIn, WithCommonServiceFields):
    type: ServiceType


# === AD-INSERTION SERVICE Models ===


class VodAdInsertionModel(BaseModel):
    adServer: AdServerSource


class VodAdInsertionModelIn(BaseModel):
    adServer: BaseResource


class LiveAdReplacementModel(BaseModel):
    adServer: AdServerSource
    gapFiller: Optional[SlateSource] = None


class LiveAdReplacementModelIn(BaseModel):
    adServer: BaseResource
    gapFiller: Optional[BaseResource] = None


class AdBreakInsertionModel(BaseModel):
    adServer: AdServerSource
    gapFiller: Optional[SlateSource] = None


class AdBreakInsertionModelIn(BaseModel):
    adServer: BaseResource
    gapFiller: Optional[BaseResource] = None


class LiveAdPreRollModel(BaseModel):
    adServer: AdServerSource
    maxDuration: Optional[float]
    offset: Optional[float]


class LiveAdPreRollModelIn(BaseModel):
    adServer: BaseResource
    maxDuration: Optional[float]
    offset: Optional[float]


class WithCommonAdInsertionServiceFields(BaseModel):
    enableAdTranscoding: Optional[bool] = False
    enableServerSideAdTracking: Optional[bool] = False
    enableSSATCheckChunk: Optional[bool] = False

    transcodingProfile: Optional[TranscodingProfileId] = None

    @property
    def sub_type(self):
        for prop in ["vodAdInsertion", "liveAdPreRoll", "liveAdReplacement"]:
            if getattr(self, prop):
                return prop

    @property
    def full_url(self):
        return self.make_full_url()

    def make_full_url(self, extra=None, *args, **kwargs):
        if extra:
            return urljoin(self.url, extra)

        return self.url


class AdInsertionServiceIn(ServiceIn, WithCommonAdInsertionServiceFields):
    vodAdInsertion: Optional[VodAdInsertionModelIn] = None
    liveAdPreRoll: Optional[LiveAdPreRollModelIn] = None
    liveAdReplacement: Optional[LiveAdReplacementModelIn] = None

    # TODO: parse the specific sub-type of source
    source: BaseResource


class AdInsertionService(
    WithCommonAdInsertionServiceFields, WithCommonServiceFields, ServiceIn
):
    vodAdInsertion: Optional[VodAdInsertionModel] = None
    liveAdPreRoll: Optional[LiveAdPreRollModel] = None
    liveAdReplacement: Optional[LiveAdReplacementModel] = None

    # TODO: parse the specific sub-type of source
    source: SourceSparse

    @property
    def type(self):
        return ServiceType.AD_INSERTION


# === CONTENT-REPLACEMENT SERVICE Models ===


class ContentReplacementServiceIn(ServiceIn):
    # TODO: parse the specific sub-type of source
    source: BaseResource
    replacement: BaseResource


class ContentReplacementService(WithCommonServiceFields, ServiceIn):
    source: SourceSparse
    replacement: SourceSparse

    @property
    def type(self):
        return ServiceType.CONTENT_REPLACEMENT


# === VIRTUAL-CHANNEL SERVICE Models ===


class WithCommonVirtualChannelServiceFields(BaseModel):
    enableAdTranscoding: Optional[bool] = False
    enableServerSideAdTracking: Optional[bool] = False
    enableSSATCheckChunk: Optional[bool] = False

    transcodingProfile: Optional[TranscodingProfileId] = None


class VirtualChannelServiceIn(ServiceIn, WithCommonVirtualChannelServiceFields):
    # TODO: parse the specific sub-type of source
    baseLive: BaseResource

    adBreakInsertion: Optional[AdBreakInsertionModelIn] = None


class VirtualChannelService(
    WithCommonVirtualChannelServiceFields, WithCommonServiceFields, ServiceIn
):
    baseLive: SourceSparse

    adBreakInsertion: Optional[AdBreakInsertionModel] = None

    @property
    def type(self):
        return ServiceType.VIRTUAL_CHANNEL
