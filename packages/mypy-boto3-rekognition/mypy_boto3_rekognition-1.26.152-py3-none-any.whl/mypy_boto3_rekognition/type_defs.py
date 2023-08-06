"""
Type annotations for rekognition service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_rekognition/type_defs/)

Usage::

    ```python
    from mypy_boto3_rekognition.type_defs import AgeRangeTypeDef

    data: AgeRangeTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Mapping, Sequence, Union

from botocore.response import StreamingBody

from .literals import (
    AttributeType,
    BodyPartType,
    CelebrityRecognitionSortByType,
    ContentClassifierType,
    ContentModerationAggregateByType,
    ContentModerationSortByType,
    DatasetStatusMessageCodeType,
    DatasetStatusType,
    DatasetTypeType,
    DetectLabelsFeatureNameType,
    EmotionNameType,
    FaceAttributesType,
    FaceSearchSortByType,
    GenderTypeType,
    KnownGenderTypeType,
    LabelDetectionAggregateByType,
    LabelDetectionSortByType,
    LandmarkTypeType,
    LivenessSessionStatusType,
    OrientationCorrectionType,
    PersonTrackingSortByType,
    ProjectStatusType,
    ProjectVersionStatusType,
    ProtectiveEquipmentTypeType,
    QualityFilterType,
    ReasonType,
    SegmentTypeType,
    StreamProcessorParameterToDeleteType,
    StreamProcessorStatusType,
    TechnicalCueTypeType,
    TextTypesType,
    UnsearchedFaceReasonType,
    UnsuccessfulFaceAssociationReasonType,
    UnsuccessfulFaceDeletionReasonType,
    UnsuccessfulFaceDisassociationReasonType,
    UserStatusType,
    VideoColorRangeType,
    VideoJobStatusType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AgeRangeTypeDef",
    "AssociateFacesRequestRequestTypeDef",
    "AssociatedFaceTypeDef",
    "UnsuccessfulFaceAssociationTypeDef",
    "AudioMetadataTypeDef",
    "BoundingBoxTypeDef",
    "S3ObjectTypeDef",
    "BeardTypeDef",
    "BlackFrameTypeDef",
    "KnownGenderTypeDef",
    "EmotionTypeDef",
    "ImageQualityTypeDef",
    "LandmarkTypeDef",
    "PoseTypeDef",
    "SmileTypeDef",
    "ConnectedHomeSettingsForUpdateTypeDef",
    "ConnectedHomeSettingsTypeDef",
    "ModerationLabelTypeDef",
    "OutputConfigTypeDef",
    "CopyProjectVersionResponseTypeDef",
    "CoversBodyPartTypeDef",
    "CreateCollectionRequestRequestTypeDef",
    "CreateCollectionResponseTypeDef",
    "CreateDatasetResponseTypeDef",
    "LivenessOutputConfigTypeDef",
    "CreateFaceLivenessSessionResponseTypeDef",
    "CreateProjectRequestRequestTypeDef",
    "CreateProjectResponseTypeDef",
    "CreateProjectVersionResponseTypeDef",
    "StreamProcessorDataSharingPreferenceTypeDef",
    "StreamProcessorNotificationChannelTypeDef",
    "CreateStreamProcessorResponseTypeDef",
    "CreateUserRequestRequestTypeDef",
    "DatasetChangesTypeDef",
    "DatasetStatsTypeDef",
    "DatasetLabelStatsTypeDef",
    "DatasetMetadataTypeDef",
    "DeleteCollectionRequestRequestTypeDef",
    "DeleteCollectionResponseTypeDef",
    "DeleteDatasetRequestRequestTypeDef",
    "DeleteFacesRequestRequestTypeDef",
    "UnsuccessfulFaceDeletionTypeDef",
    "DeleteProjectPolicyRequestRequestTypeDef",
    "DeleteProjectRequestRequestTypeDef",
    "DeleteProjectResponseTypeDef",
    "DeleteProjectVersionRequestRequestTypeDef",
    "DeleteProjectVersionResponseTypeDef",
    "DeleteStreamProcessorRequestRequestTypeDef",
    "DeleteUserRequestRequestTypeDef",
    "DescribeCollectionRequestRequestTypeDef",
    "DescribeCollectionResponseTypeDef",
    "DescribeDatasetRequestRequestTypeDef",
    "DescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef",
    "WaiterConfigTypeDef",
    "DescribeProjectVersionsRequestRequestTypeDef",
    "DescribeProjectsRequestDescribeProjectsPaginateTypeDef",
    "DescribeProjectsRequestRequestTypeDef",
    "DescribeStreamProcessorRequestRequestTypeDef",
    "DetectLabelsImageQualityTypeDef",
    "DominantColorTypeDef",
    "DetectLabelsImagePropertiesSettingsTypeDef",
    "GeneralLabelsSettingsTypeDef",
    "HumanLoopActivationOutputTypeDef",
    "ProtectiveEquipmentSummarizationAttributesTypeDef",
    "ProtectiveEquipmentSummaryTypeDef",
    "DetectionFilterTypeDef",
    "DisassociateFacesRequestRequestTypeDef",
    "DisassociatedFaceTypeDef",
    "UnsuccessfulFaceDisassociationTypeDef",
    "DistributeDatasetTypeDef",
    "EyeDirectionTypeDef",
    "EyeOpenTypeDef",
    "EyeglassesTypeDef",
    "FaceOccludedTypeDef",
    "GenderTypeDef",
    "MouthOpenTypeDef",
    "MustacheTypeDef",
    "SunglassesTypeDef",
    "FaceSearchSettingsTypeDef",
    "PointTypeDef",
    "GetCelebrityInfoRequestRequestTypeDef",
    "GetCelebrityRecognitionRequestRequestTypeDef",
    "VideoMetadataTypeDef",
    "GetContentModerationRequestMetadataTypeDef",
    "GetContentModerationRequestRequestTypeDef",
    "GetFaceDetectionRequestRequestTypeDef",
    "GetFaceLivenessSessionResultsRequestRequestTypeDef",
    "GetFaceSearchRequestRequestTypeDef",
    "GetLabelDetectionRequestMetadataTypeDef",
    "GetLabelDetectionRequestRequestTypeDef",
    "GetPersonTrackingRequestRequestTypeDef",
    "GetSegmentDetectionRequestRequestTypeDef",
    "SegmentTypeInfoTypeDef",
    "GetTextDetectionRequestRequestTypeDef",
    "HumanLoopDataAttributesTypeDef",
    "KinesisDataStreamTypeDef",
    "KinesisVideoStreamStartSelectorTypeDef",
    "KinesisVideoStreamTypeDef",
    "LabelAliasTypeDef",
    "LabelCategoryTypeDef",
    "ParentTypeDef",
    "ListCollectionsRequestListCollectionsPaginateTypeDef",
    "ListCollectionsRequestRequestTypeDef",
    "ListCollectionsResponseTypeDef",
    "ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    "ListDatasetEntriesRequestRequestTypeDef",
    "ListDatasetEntriesResponseTypeDef",
    "ListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef",
    "ListDatasetLabelsRequestRequestTypeDef",
    "ListFacesRequestListFacesPaginateTypeDef",
    "ListFacesRequestRequestTypeDef",
    "ListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef",
    "ListProjectPoliciesRequestRequestTypeDef",
    "ProjectPolicyTypeDef",
    "ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef",
    "ListStreamProcessorsRequestRequestTypeDef",
    "StreamProcessorTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListUsersRequestListUsersPaginateTypeDef",
    "ListUsersRequestRequestTypeDef",
    "UserTypeDef",
    "MatchedUserTypeDef",
    "NotificationChannelTypeDef",
    "PaginatorConfigTypeDef",
    "PutProjectPolicyRequestRequestTypeDef",
    "PutProjectPolicyResponseTypeDef",
    "ResponseMetadataTypeDef",
    "S3DestinationTypeDef",
    "SearchFacesRequestRequestTypeDef",
    "SearchUsersRequestRequestTypeDef",
    "SearchedFaceTypeDef",
    "SearchedUserTypeDef",
    "ShotSegmentTypeDef",
    "TechnicalCueSegmentTypeDef",
    "StartCelebrityRecognitionResponseTypeDef",
    "StartContentModerationResponseTypeDef",
    "StartFaceDetectionResponseTypeDef",
    "StartFaceSearchResponseTypeDef",
    "StartLabelDetectionResponseTypeDef",
    "StartPersonTrackingResponseTypeDef",
    "StartProjectVersionRequestRequestTypeDef",
    "StartProjectVersionResponseTypeDef",
    "StartShotDetectionFilterTypeDef",
    "StartSegmentDetectionResponseTypeDef",
    "StreamProcessingStopSelectorTypeDef",
    "StartStreamProcessorResponseTypeDef",
    "StartTextDetectionResponseTypeDef",
    "StopProjectVersionRequestRequestTypeDef",
    "StopProjectVersionResponseTypeDef",
    "StopStreamProcessorRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "AssociateFacesResponseTypeDef",
    "ComparedSourceImageFaceTypeDef",
    "FaceTypeDef",
    "AuditImageTypeDef",
    "GroundTruthManifestTypeDef",
    "ImageTypeDef",
    "SummaryTypeDef",
    "VideoTypeDef",
    "StartTechnicalCueDetectionFilterTypeDef",
    "GetCelebrityInfoResponseTypeDef",
    "ComparedFaceTypeDef",
    "StreamProcessorSettingsForUpdateTypeDef",
    "ContentModerationDetectionTypeDef",
    "CopyProjectVersionRequestRequestTypeDef",
    "EquipmentDetectionTypeDef",
    "CreateFaceLivenessSessionRequestSettingsTypeDef",
    "UpdateDatasetEntriesRequestRequestTypeDef",
    "DatasetDescriptionTypeDef",
    "DatasetLabelDescriptionTypeDef",
    "ProjectDescriptionTypeDef",
    "DeleteFacesResponseTypeDef",
    "DescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef",
    "DescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef",
    "DetectLabelsImageBackgroundTypeDef",
    "DetectLabelsImageForegroundTypeDef",
    "InstanceTypeDef",
    "DetectLabelsSettingsTypeDef",
    "LabelDetectionSettingsTypeDef",
    "DetectModerationLabelsResponseTypeDef",
    "DisassociateFacesResponseTypeDef",
    "DistributeDatasetEntriesRequestRequestTypeDef",
    "FaceDetailTypeDef",
    "StreamProcessorSettingsTypeDef",
    "GeometryTypeDef",
    "RegionOfInterestTypeDef",
    "HumanLoopConfigTypeDef",
    "StreamProcessingStartSelectorTypeDef",
    "StreamProcessorInputTypeDef",
    "ListProjectPoliciesResponseTypeDef",
    "ListStreamProcessorsResponseTypeDef",
    "ListUsersResponseTypeDef",
    "UserMatchTypeDef",
    "StreamProcessorOutputTypeDef",
    "SegmentDetectionTypeDef",
    "FaceMatchTypeDef",
    "ListFacesResponseTypeDef",
    "GetFaceLivenessSessionResultsResponseTypeDef",
    "AssetTypeDef",
    "DatasetSourceTypeDef",
    "CompareFacesRequestRequestTypeDef",
    "DetectCustomLabelsRequestRequestTypeDef",
    "DetectFacesRequestRequestTypeDef",
    "DetectProtectiveEquipmentRequestRequestTypeDef",
    "IndexFacesRequestRequestTypeDef",
    "RecognizeCelebritiesRequestRequestTypeDef",
    "SearchFacesByImageRequestRequestTypeDef",
    "SearchUsersByImageRequestRequestTypeDef",
    "EvaluationResultTypeDef",
    "StartCelebrityRecognitionRequestRequestTypeDef",
    "StartContentModerationRequestRequestTypeDef",
    "StartFaceDetectionRequestRequestTypeDef",
    "StartFaceSearchRequestRequestTypeDef",
    "StartPersonTrackingRequestRequestTypeDef",
    "StartSegmentDetectionFiltersTypeDef",
    "CelebrityTypeDef",
    "CompareFacesMatchTypeDef",
    "GetContentModerationResponseTypeDef",
    "ProtectiveEquipmentBodyPartTypeDef",
    "CreateFaceLivenessSessionRequestRequestTypeDef",
    "DescribeDatasetResponseTypeDef",
    "ListDatasetLabelsResponseTypeDef",
    "DescribeProjectsResponseTypeDef",
    "DetectLabelsImagePropertiesTypeDef",
    "LabelTypeDef",
    "DetectLabelsRequestRequestTypeDef",
    "StartLabelDetectionRequestRequestTypeDef",
    "CelebrityDetailTypeDef",
    "DetectFacesResponseTypeDef",
    "FaceDetectionTypeDef",
    "FaceRecordTypeDef",
    "PersonDetailTypeDef",
    "SearchedFaceDetailsTypeDef",
    "UnindexedFaceTypeDef",
    "UnsearchedFaceTypeDef",
    "CustomLabelTypeDef",
    "TextDetectionTypeDef",
    "DetectTextFiltersTypeDef",
    "StartTextDetectionFiltersTypeDef",
    "UpdateStreamProcessorRequestRequestTypeDef",
    "DetectModerationLabelsRequestRequestTypeDef",
    "StartStreamProcessorRequestRequestTypeDef",
    "SearchUsersResponseTypeDef",
    "CreateStreamProcessorRequestRequestTypeDef",
    "DescribeStreamProcessorResponseTypeDef",
    "GetSegmentDetectionResponseTypeDef",
    "SearchFacesByImageResponseTypeDef",
    "SearchFacesResponseTypeDef",
    "TestingDataTypeDef",
    "TrainingDataTypeDef",
    "ValidationDataTypeDef",
    "CreateDatasetRequestRequestTypeDef",
    "StartSegmentDetectionRequestRequestTypeDef",
    "RecognizeCelebritiesResponseTypeDef",
    "CompareFacesResponseTypeDef",
    "ProtectiveEquipmentPersonTypeDef",
    "DetectLabelsResponseTypeDef",
    "LabelDetectionTypeDef",
    "CelebrityRecognitionTypeDef",
    "GetFaceDetectionResponseTypeDef",
    "PersonDetectionTypeDef",
    "PersonMatchTypeDef",
    "IndexFacesResponseTypeDef",
    "SearchUsersByImageResponseTypeDef",
    "DetectCustomLabelsResponseTypeDef",
    "DetectTextResponseTypeDef",
    "TextDetectionResultTypeDef",
    "DetectTextRequestRequestTypeDef",
    "StartTextDetectionRequestRequestTypeDef",
    "CreateProjectVersionRequestRequestTypeDef",
    "TestingDataResultTypeDef",
    "TrainingDataResultTypeDef",
    "DetectProtectiveEquipmentResponseTypeDef",
    "GetLabelDetectionResponseTypeDef",
    "GetCelebrityRecognitionResponseTypeDef",
    "GetPersonTrackingResponseTypeDef",
    "GetFaceSearchResponseTypeDef",
    "GetTextDetectionResponseTypeDef",
    "ProjectVersionDescriptionTypeDef",
    "DescribeProjectVersionsResponseTypeDef",
)

AgeRangeTypeDef = TypedDict(
    "AgeRangeTypeDef",
    {
        "Low": int,
        "High": int,
    },
    total=False,
)

_RequiredAssociateFacesRequestRequestTypeDef = TypedDict(
    "_RequiredAssociateFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
        "UserId": str,
        "FaceIds": Sequence[str],
    },
)
_OptionalAssociateFacesRequestRequestTypeDef = TypedDict(
    "_OptionalAssociateFacesRequestRequestTypeDef",
    {
        "UserMatchThreshold": float,
        "ClientRequestToken": str,
    },
    total=False,
)


class AssociateFacesRequestRequestTypeDef(
    _RequiredAssociateFacesRequestRequestTypeDef, _OptionalAssociateFacesRequestRequestTypeDef
):
    pass


AssociatedFaceTypeDef = TypedDict(
    "AssociatedFaceTypeDef",
    {
        "FaceId": str,
    },
    total=False,
)

UnsuccessfulFaceAssociationTypeDef = TypedDict(
    "UnsuccessfulFaceAssociationTypeDef",
    {
        "FaceId": str,
        "UserId": str,
        "Confidence": float,
        "Reasons": List[UnsuccessfulFaceAssociationReasonType],
    },
    total=False,
)

AudioMetadataTypeDef = TypedDict(
    "AudioMetadataTypeDef",
    {
        "Codec": str,
        "DurationMillis": int,
        "SampleRate": int,
        "NumberOfChannels": int,
    },
    total=False,
)

BoundingBoxTypeDef = TypedDict(
    "BoundingBoxTypeDef",
    {
        "Width": float,
        "Height": float,
        "Left": float,
        "Top": float,
    },
    total=False,
)

S3ObjectTypeDef = TypedDict(
    "S3ObjectTypeDef",
    {
        "Bucket": str,
        "Name": str,
        "Version": str,
    },
    total=False,
)

BeardTypeDef = TypedDict(
    "BeardTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

BlackFrameTypeDef = TypedDict(
    "BlackFrameTypeDef",
    {
        "MaxPixelThreshold": float,
        "MinCoveragePercentage": float,
    },
    total=False,
)

KnownGenderTypeDef = TypedDict(
    "KnownGenderTypeDef",
    {
        "Type": KnownGenderTypeType,
    },
    total=False,
)

EmotionTypeDef = TypedDict(
    "EmotionTypeDef",
    {
        "Type": EmotionNameType,
        "Confidence": float,
    },
    total=False,
)

ImageQualityTypeDef = TypedDict(
    "ImageQualityTypeDef",
    {
        "Brightness": float,
        "Sharpness": float,
    },
    total=False,
)

LandmarkTypeDef = TypedDict(
    "LandmarkTypeDef",
    {
        "Type": LandmarkTypeType,
        "X": float,
        "Y": float,
    },
    total=False,
)

PoseTypeDef = TypedDict(
    "PoseTypeDef",
    {
        "Roll": float,
        "Yaw": float,
        "Pitch": float,
    },
    total=False,
)

SmileTypeDef = TypedDict(
    "SmileTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

ConnectedHomeSettingsForUpdateTypeDef = TypedDict(
    "ConnectedHomeSettingsForUpdateTypeDef",
    {
        "Labels": Sequence[str],
        "MinConfidence": float,
    },
    total=False,
)

_RequiredConnectedHomeSettingsTypeDef = TypedDict(
    "_RequiredConnectedHomeSettingsTypeDef",
    {
        "Labels": Sequence[str],
    },
)
_OptionalConnectedHomeSettingsTypeDef = TypedDict(
    "_OptionalConnectedHomeSettingsTypeDef",
    {
        "MinConfidence": float,
    },
    total=False,
)


class ConnectedHomeSettingsTypeDef(
    _RequiredConnectedHomeSettingsTypeDef, _OptionalConnectedHomeSettingsTypeDef
):
    pass


ModerationLabelTypeDef = TypedDict(
    "ModerationLabelTypeDef",
    {
        "Confidence": float,
        "Name": str,
        "ParentName": str,
    },
    total=False,
)

OutputConfigTypeDef = TypedDict(
    "OutputConfigTypeDef",
    {
        "S3Bucket": str,
        "S3KeyPrefix": str,
    },
    total=False,
)

CopyProjectVersionResponseTypeDef = TypedDict(
    "CopyProjectVersionResponseTypeDef",
    {
        "ProjectVersionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CoversBodyPartTypeDef = TypedDict(
    "CoversBodyPartTypeDef",
    {
        "Confidence": float,
        "Value": bool,
    },
    total=False,
)

_RequiredCreateCollectionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCollectionRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalCreateCollectionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCollectionRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
    },
    total=False,
)


class CreateCollectionRequestRequestTypeDef(
    _RequiredCreateCollectionRequestRequestTypeDef, _OptionalCreateCollectionRequestRequestTypeDef
):
    pass


CreateCollectionResponseTypeDef = TypedDict(
    "CreateCollectionResponseTypeDef",
    {
        "StatusCode": int,
        "CollectionArn": str,
        "FaceModelVersion": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDatasetResponseTypeDef = TypedDict(
    "CreateDatasetResponseTypeDef",
    {
        "DatasetArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredLivenessOutputConfigTypeDef = TypedDict(
    "_RequiredLivenessOutputConfigTypeDef",
    {
        "S3Bucket": str,
    },
)
_OptionalLivenessOutputConfigTypeDef = TypedDict(
    "_OptionalLivenessOutputConfigTypeDef",
    {
        "S3KeyPrefix": str,
    },
    total=False,
)


class LivenessOutputConfigTypeDef(
    _RequiredLivenessOutputConfigTypeDef, _OptionalLivenessOutputConfigTypeDef
):
    pass


CreateFaceLivenessSessionResponseTypeDef = TypedDict(
    "CreateFaceLivenessSessionResponseTypeDef",
    {
        "SessionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateProjectRequestRequestTypeDef = TypedDict(
    "CreateProjectRequestRequestTypeDef",
    {
        "ProjectName": str,
    },
)

CreateProjectResponseTypeDef = TypedDict(
    "CreateProjectResponseTypeDef",
    {
        "ProjectArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateProjectVersionResponseTypeDef = TypedDict(
    "CreateProjectVersionResponseTypeDef",
    {
        "ProjectVersionArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StreamProcessorDataSharingPreferenceTypeDef = TypedDict(
    "StreamProcessorDataSharingPreferenceTypeDef",
    {
        "OptIn": bool,
    },
)

StreamProcessorNotificationChannelTypeDef = TypedDict(
    "StreamProcessorNotificationChannelTypeDef",
    {
        "SNSTopicArn": str,
    },
)

CreateStreamProcessorResponseTypeDef = TypedDict(
    "CreateStreamProcessorResponseTypeDef",
    {
        "StreamProcessorArn": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateUserRequestRequestTypeDef = TypedDict(
    "_RequiredCreateUserRequestRequestTypeDef",
    {
        "CollectionId": str,
        "UserId": str,
    },
)
_OptionalCreateUserRequestRequestTypeDef = TypedDict(
    "_OptionalCreateUserRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class CreateUserRequestRequestTypeDef(
    _RequiredCreateUserRequestRequestTypeDef, _OptionalCreateUserRequestRequestTypeDef
):
    pass


DatasetChangesTypeDef = TypedDict(
    "DatasetChangesTypeDef",
    {
        "GroundTruth": Union[str, bytes, IO[Any], StreamingBody],
    },
)

DatasetStatsTypeDef = TypedDict(
    "DatasetStatsTypeDef",
    {
        "LabeledEntries": int,
        "TotalEntries": int,
        "TotalLabels": int,
        "ErrorEntries": int,
    },
    total=False,
)

DatasetLabelStatsTypeDef = TypedDict(
    "DatasetLabelStatsTypeDef",
    {
        "EntryCount": int,
        "BoundingBoxCount": int,
    },
    total=False,
)

DatasetMetadataTypeDef = TypedDict(
    "DatasetMetadataTypeDef",
    {
        "CreationTimestamp": datetime,
        "DatasetType": DatasetTypeType,
        "DatasetArn": str,
        "Status": DatasetStatusType,
        "StatusMessage": str,
        "StatusMessageCode": DatasetStatusMessageCodeType,
    },
    total=False,
)

DeleteCollectionRequestRequestTypeDef = TypedDict(
    "DeleteCollectionRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)

DeleteCollectionResponseTypeDef = TypedDict(
    "DeleteCollectionResponseTypeDef",
    {
        "StatusCode": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteDatasetRequestRequestTypeDef = TypedDict(
    "DeleteDatasetRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)

DeleteFacesRequestRequestTypeDef = TypedDict(
    "DeleteFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
        "FaceIds": Sequence[str],
    },
)

UnsuccessfulFaceDeletionTypeDef = TypedDict(
    "UnsuccessfulFaceDeletionTypeDef",
    {
        "FaceId": str,
        "UserId": str,
        "Reasons": List[UnsuccessfulFaceDeletionReasonType],
    },
    total=False,
)

_RequiredDeleteProjectPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteProjectPolicyRequestRequestTypeDef",
    {
        "ProjectArn": str,
        "PolicyName": str,
    },
)
_OptionalDeleteProjectPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteProjectPolicyRequestRequestTypeDef",
    {
        "PolicyRevisionId": str,
    },
    total=False,
)


class DeleteProjectPolicyRequestRequestTypeDef(
    _RequiredDeleteProjectPolicyRequestRequestTypeDef,
    _OptionalDeleteProjectPolicyRequestRequestTypeDef,
):
    pass


DeleteProjectRequestRequestTypeDef = TypedDict(
    "DeleteProjectRequestRequestTypeDef",
    {
        "ProjectArn": str,
    },
)

DeleteProjectResponseTypeDef = TypedDict(
    "DeleteProjectResponseTypeDef",
    {
        "Status": ProjectStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteProjectVersionRequestRequestTypeDef = TypedDict(
    "DeleteProjectVersionRequestRequestTypeDef",
    {
        "ProjectVersionArn": str,
    },
)

DeleteProjectVersionResponseTypeDef = TypedDict(
    "DeleteProjectVersionResponseTypeDef",
    {
        "Status": ProjectVersionStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteStreamProcessorRequestRequestTypeDef = TypedDict(
    "DeleteStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)

_RequiredDeleteUserRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteUserRequestRequestTypeDef",
    {
        "CollectionId": str,
        "UserId": str,
    },
)
_OptionalDeleteUserRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteUserRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class DeleteUserRequestRequestTypeDef(
    _RequiredDeleteUserRequestRequestTypeDef, _OptionalDeleteUserRequestRequestTypeDef
):
    pass


DescribeCollectionRequestRequestTypeDef = TypedDict(
    "DescribeCollectionRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)

DescribeCollectionResponseTypeDef = TypedDict(
    "DescribeCollectionResponseTypeDef",
    {
        "FaceCount": int,
        "FaceModelVersion": str,
        "CollectionARN": str,
        "CreationTimestamp": datetime,
        "UserCount": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeDatasetRequestRequestTypeDef = TypedDict(
    "DescribeDatasetRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)

_RequiredDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef = TypedDict(
    "_RequiredDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef = TypedDict(
    "_OptionalDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef",
    {
        "VersionNames": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class DescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef(
    _RequiredDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef,
    _OptionalDescribeProjectVersionsRequestDescribeProjectVersionsPaginateTypeDef,
):
    pass


WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef",
    {
        "Delay": int,
        "MaxAttempts": int,
    },
    total=False,
)

_RequiredDescribeProjectVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredDescribeProjectVersionsRequestRequestTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalDescribeProjectVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalDescribeProjectVersionsRequestRequestTypeDef",
    {
        "VersionNames": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class DescribeProjectVersionsRequestRequestTypeDef(
    _RequiredDescribeProjectVersionsRequestRequestTypeDef,
    _OptionalDescribeProjectVersionsRequestRequestTypeDef,
):
    pass


DescribeProjectsRequestDescribeProjectsPaginateTypeDef = TypedDict(
    "DescribeProjectsRequestDescribeProjectsPaginateTypeDef",
    {
        "ProjectNames": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

DescribeProjectsRequestRequestTypeDef = TypedDict(
    "DescribeProjectsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "ProjectNames": Sequence[str],
    },
    total=False,
)

DescribeStreamProcessorRequestRequestTypeDef = TypedDict(
    "DescribeStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)

DetectLabelsImageQualityTypeDef = TypedDict(
    "DetectLabelsImageQualityTypeDef",
    {
        "Brightness": float,
        "Sharpness": float,
        "Contrast": float,
    },
    total=False,
)

DominantColorTypeDef = TypedDict(
    "DominantColorTypeDef",
    {
        "Red": int,
        "Blue": int,
        "Green": int,
        "HexCode": str,
        "CSSColor": str,
        "SimplifiedColor": str,
        "PixelPercent": float,
    },
    total=False,
)

DetectLabelsImagePropertiesSettingsTypeDef = TypedDict(
    "DetectLabelsImagePropertiesSettingsTypeDef",
    {
        "MaxDominantColors": int,
    },
    total=False,
)

GeneralLabelsSettingsTypeDef = TypedDict(
    "GeneralLabelsSettingsTypeDef",
    {
        "LabelInclusionFilters": Sequence[str],
        "LabelExclusionFilters": Sequence[str],
        "LabelCategoryInclusionFilters": Sequence[str],
        "LabelCategoryExclusionFilters": Sequence[str],
    },
    total=False,
)

HumanLoopActivationOutputTypeDef = TypedDict(
    "HumanLoopActivationOutputTypeDef",
    {
        "HumanLoopArn": str,
        "HumanLoopActivationReasons": List[str],
        "HumanLoopActivationConditionsEvaluationResults": str,
    },
    total=False,
)

ProtectiveEquipmentSummarizationAttributesTypeDef = TypedDict(
    "ProtectiveEquipmentSummarizationAttributesTypeDef",
    {
        "MinConfidence": float,
        "RequiredEquipmentTypes": Sequence[ProtectiveEquipmentTypeType],
    },
)

ProtectiveEquipmentSummaryTypeDef = TypedDict(
    "ProtectiveEquipmentSummaryTypeDef",
    {
        "PersonsWithRequiredEquipment": List[int],
        "PersonsWithoutRequiredEquipment": List[int],
        "PersonsIndeterminate": List[int],
    },
    total=False,
)

DetectionFilterTypeDef = TypedDict(
    "DetectionFilterTypeDef",
    {
        "MinConfidence": float,
        "MinBoundingBoxHeight": float,
        "MinBoundingBoxWidth": float,
    },
    total=False,
)

_RequiredDisassociateFacesRequestRequestTypeDef = TypedDict(
    "_RequiredDisassociateFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
        "UserId": str,
        "FaceIds": Sequence[str],
    },
)
_OptionalDisassociateFacesRequestRequestTypeDef = TypedDict(
    "_OptionalDisassociateFacesRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
    },
    total=False,
)


class DisassociateFacesRequestRequestTypeDef(
    _RequiredDisassociateFacesRequestRequestTypeDef, _OptionalDisassociateFacesRequestRequestTypeDef
):
    pass


DisassociatedFaceTypeDef = TypedDict(
    "DisassociatedFaceTypeDef",
    {
        "FaceId": str,
    },
    total=False,
)

UnsuccessfulFaceDisassociationTypeDef = TypedDict(
    "UnsuccessfulFaceDisassociationTypeDef",
    {
        "FaceId": str,
        "UserId": str,
        "Reasons": List[UnsuccessfulFaceDisassociationReasonType],
    },
    total=False,
)

DistributeDatasetTypeDef = TypedDict(
    "DistributeDatasetTypeDef",
    {
        "Arn": str,
    },
)

EyeDirectionTypeDef = TypedDict(
    "EyeDirectionTypeDef",
    {
        "Yaw": float,
        "Pitch": float,
        "Confidence": float,
    },
    total=False,
)

EyeOpenTypeDef = TypedDict(
    "EyeOpenTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

EyeglassesTypeDef = TypedDict(
    "EyeglassesTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

FaceOccludedTypeDef = TypedDict(
    "FaceOccludedTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

GenderTypeDef = TypedDict(
    "GenderTypeDef",
    {
        "Value": GenderTypeType,
        "Confidence": float,
    },
    total=False,
)

MouthOpenTypeDef = TypedDict(
    "MouthOpenTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

MustacheTypeDef = TypedDict(
    "MustacheTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

SunglassesTypeDef = TypedDict(
    "SunglassesTypeDef",
    {
        "Value": bool,
        "Confidence": float,
    },
    total=False,
)

FaceSearchSettingsTypeDef = TypedDict(
    "FaceSearchSettingsTypeDef",
    {
        "CollectionId": str,
        "FaceMatchThreshold": float,
    },
    total=False,
)

PointTypeDef = TypedDict(
    "PointTypeDef",
    {
        "X": float,
        "Y": float,
    },
    total=False,
)

GetCelebrityInfoRequestRequestTypeDef = TypedDict(
    "GetCelebrityInfoRequestRequestTypeDef",
    {
        "Id": str,
    },
)

_RequiredGetCelebrityRecognitionRequestRequestTypeDef = TypedDict(
    "_RequiredGetCelebrityRecognitionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetCelebrityRecognitionRequestRequestTypeDef = TypedDict(
    "_OptionalGetCelebrityRecognitionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": CelebrityRecognitionSortByType,
    },
    total=False,
)


class GetCelebrityRecognitionRequestRequestTypeDef(
    _RequiredGetCelebrityRecognitionRequestRequestTypeDef,
    _OptionalGetCelebrityRecognitionRequestRequestTypeDef,
):
    pass


VideoMetadataTypeDef = TypedDict(
    "VideoMetadataTypeDef",
    {
        "Codec": str,
        "DurationMillis": int,
        "Format": str,
        "FrameRate": float,
        "FrameHeight": int,
        "FrameWidth": int,
        "ColorRange": VideoColorRangeType,
    },
    total=False,
)

GetContentModerationRequestMetadataTypeDef = TypedDict(
    "GetContentModerationRequestMetadataTypeDef",
    {
        "SortBy": ContentModerationSortByType,
        "AggregateBy": ContentModerationAggregateByType,
    },
    total=False,
)

_RequiredGetContentModerationRequestRequestTypeDef = TypedDict(
    "_RequiredGetContentModerationRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetContentModerationRequestRequestTypeDef = TypedDict(
    "_OptionalGetContentModerationRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": ContentModerationSortByType,
        "AggregateBy": ContentModerationAggregateByType,
    },
    total=False,
)


class GetContentModerationRequestRequestTypeDef(
    _RequiredGetContentModerationRequestRequestTypeDef,
    _OptionalGetContentModerationRequestRequestTypeDef,
):
    pass


_RequiredGetFaceDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetFaceDetectionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetFaceDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetFaceDetectionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetFaceDetectionRequestRequestTypeDef(
    _RequiredGetFaceDetectionRequestRequestTypeDef, _OptionalGetFaceDetectionRequestRequestTypeDef
):
    pass


GetFaceLivenessSessionResultsRequestRequestTypeDef = TypedDict(
    "GetFaceLivenessSessionResultsRequestRequestTypeDef",
    {
        "SessionId": str,
    },
)

_RequiredGetFaceSearchRequestRequestTypeDef = TypedDict(
    "_RequiredGetFaceSearchRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetFaceSearchRequestRequestTypeDef = TypedDict(
    "_OptionalGetFaceSearchRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": FaceSearchSortByType,
    },
    total=False,
)


class GetFaceSearchRequestRequestTypeDef(
    _RequiredGetFaceSearchRequestRequestTypeDef, _OptionalGetFaceSearchRequestRequestTypeDef
):
    pass


GetLabelDetectionRequestMetadataTypeDef = TypedDict(
    "GetLabelDetectionRequestMetadataTypeDef",
    {
        "SortBy": LabelDetectionSortByType,
        "AggregateBy": LabelDetectionAggregateByType,
    },
    total=False,
)

_RequiredGetLabelDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetLabelDetectionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetLabelDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetLabelDetectionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": LabelDetectionSortByType,
        "AggregateBy": LabelDetectionAggregateByType,
    },
    total=False,
)


class GetLabelDetectionRequestRequestTypeDef(
    _RequiredGetLabelDetectionRequestRequestTypeDef, _OptionalGetLabelDetectionRequestRequestTypeDef
):
    pass


_RequiredGetPersonTrackingRequestRequestTypeDef = TypedDict(
    "_RequiredGetPersonTrackingRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetPersonTrackingRequestRequestTypeDef = TypedDict(
    "_OptionalGetPersonTrackingRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
        "SortBy": PersonTrackingSortByType,
    },
    total=False,
)


class GetPersonTrackingRequestRequestTypeDef(
    _RequiredGetPersonTrackingRequestRequestTypeDef, _OptionalGetPersonTrackingRequestRequestTypeDef
):
    pass


_RequiredGetSegmentDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetSegmentDetectionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetSegmentDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetSegmentDetectionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetSegmentDetectionRequestRequestTypeDef(
    _RequiredGetSegmentDetectionRequestRequestTypeDef,
    _OptionalGetSegmentDetectionRequestRequestTypeDef,
):
    pass


SegmentTypeInfoTypeDef = TypedDict(
    "SegmentTypeInfoTypeDef",
    {
        "Type": SegmentTypeType,
        "ModelVersion": str,
    },
    total=False,
)

_RequiredGetTextDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredGetTextDetectionRequestRequestTypeDef",
    {
        "JobId": str,
    },
)
_OptionalGetTextDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalGetTextDetectionRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class GetTextDetectionRequestRequestTypeDef(
    _RequiredGetTextDetectionRequestRequestTypeDef, _OptionalGetTextDetectionRequestRequestTypeDef
):
    pass


HumanLoopDataAttributesTypeDef = TypedDict(
    "HumanLoopDataAttributesTypeDef",
    {
        "ContentClassifiers": Sequence[ContentClassifierType],
    },
    total=False,
)

KinesisDataStreamTypeDef = TypedDict(
    "KinesisDataStreamTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

KinesisVideoStreamStartSelectorTypeDef = TypedDict(
    "KinesisVideoStreamStartSelectorTypeDef",
    {
        "ProducerTimestamp": int,
        "FragmentNumber": str,
    },
    total=False,
)

KinesisVideoStreamTypeDef = TypedDict(
    "KinesisVideoStreamTypeDef",
    {
        "Arn": str,
    },
    total=False,
)

LabelAliasTypeDef = TypedDict(
    "LabelAliasTypeDef",
    {
        "Name": str,
    },
    total=False,
)

LabelCategoryTypeDef = TypedDict(
    "LabelCategoryTypeDef",
    {
        "Name": str,
    },
    total=False,
)

ParentTypeDef = TypedDict(
    "ParentTypeDef",
    {
        "Name": str,
    },
    total=False,
)

ListCollectionsRequestListCollectionsPaginateTypeDef = TypedDict(
    "ListCollectionsRequestListCollectionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListCollectionsRequestRequestTypeDef = TypedDict(
    "ListCollectionsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

ListCollectionsResponseTypeDef = TypedDict(
    "ListCollectionsResponseTypeDef",
    {
        "CollectionIds": List[str],
        "NextToken": str,
        "FaceModelVersions": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef = TypedDict(
    "_RequiredListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    {
        "DatasetArn": str,
    },
)
_OptionalListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef = TypedDict(
    "_OptionalListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef",
    {
        "ContainsLabels": Sequence[str],
        "Labeled": bool,
        "SourceRefContains": str,
        "HasErrors": bool,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef(
    _RequiredListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
    _OptionalListDatasetEntriesRequestListDatasetEntriesPaginateTypeDef,
):
    pass


_RequiredListDatasetEntriesRequestRequestTypeDef = TypedDict(
    "_RequiredListDatasetEntriesRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)
_OptionalListDatasetEntriesRequestRequestTypeDef = TypedDict(
    "_OptionalListDatasetEntriesRequestRequestTypeDef",
    {
        "ContainsLabels": Sequence[str],
        "Labeled": bool,
        "SourceRefContains": str,
        "HasErrors": bool,
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDatasetEntriesRequestRequestTypeDef(
    _RequiredListDatasetEntriesRequestRequestTypeDef,
    _OptionalListDatasetEntriesRequestRequestTypeDef,
):
    pass


ListDatasetEntriesResponseTypeDef = TypedDict(
    "ListDatasetEntriesResponseTypeDef",
    {
        "DatasetEntries": List[str],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef = TypedDict(
    "_RequiredListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef",
    {
        "DatasetArn": str,
    },
)
_OptionalListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef = TypedDict(
    "_OptionalListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef(
    _RequiredListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef,
    _OptionalListDatasetLabelsRequestListDatasetLabelsPaginateTypeDef,
):
    pass


_RequiredListDatasetLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredListDatasetLabelsRequestRequestTypeDef",
    {
        "DatasetArn": str,
    },
)
_OptionalListDatasetLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalListDatasetLabelsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListDatasetLabelsRequestRequestTypeDef(
    _RequiredListDatasetLabelsRequestRequestTypeDef, _OptionalListDatasetLabelsRequestRequestTypeDef
):
    pass


_RequiredListFacesRequestListFacesPaginateTypeDef = TypedDict(
    "_RequiredListFacesRequestListFacesPaginateTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListFacesRequestListFacesPaginateTypeDef = TypedDict(
    "_OptionalListFacesRequestListFacesPaginateTypeDef",
    {
        "UserId": str,
        "FaceIds": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListFacesRequestListFacesPaginateTypeDef(
    _RequiredListFacesRequestListFacesPaginateTypeDef,
    _OptionalListFacesRequestListFacesPaginateTypeDef,
):
    pass


_RequiredListFacesRequestRequestTypeDef = TypedDict(
    "_RequiredListFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListFacesRequestRequestTypeDef = TypedDict(
    "_OptionalListFacesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
        "UserId": str,
        "FaceIds": Sequence[str],
    },
    total=False,
)


class ListFacesRequestRequestTypeDef(
    _RequiredListFacesRequestRequestTypeDef, _OptionalListFacesRequestRequestTypeDef
):
    pass


_RequiredListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef = TypedDict(
    "_RequiredListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef = TypedDict(
    "_OptionalListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef(
    _RequiredListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef,
    _OptionalListProjectPoliciesRequestListProjectPoliciesPaginateTypeDef,
):
    pass


_RequiredListProjectPoliciesRequestRequestTypeDef = TypedDict(
    "_RequiredListProjectPoliciesRequestRequestTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalListProjectPoliciesRequestRequestTypeDef = TypedDict(
    "_OptionalListProjectPoliciesRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)


class ListProjectPoliciesRequestRequestTypeDef(
    _RequiredListProjectPoliciesRequestRequestTypeDef,
    _OptionalListProjectPoliciesRequestRequestTypeDef,
):
    pass


ProjectPolicyTypeDef = TypedDict(
    "ProjectPolicyTypeDef",
    {
        "ProjectArn": str,
        "PolicyName": str,
        "PolicyRevisionId": str,
        "PolicyDocument": str,
        "CreationTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
    },
    total=False,
)

ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef = TypedDict(
    "ListStreamProcessorsRequestListStreamProcessorsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListStreamProcessorsRequestRequestTypeDef = TypedDict(
    "ListStreamProcessorsRequestRequestTypeDef",
    {
        "NextToken": str,
        "MaxResults": int,
    },
    total=False,
)

StreamProcessorTypeDef = TypedDict(
    "StreamProcessorTypeDef",
    {
        "Name": str,
        "Status": StreamProcessorStatusType,
    },
    total=False,
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "_RequiredListUsersRequestListUsersPaginateTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListUsersRequestListUsersPaginateTypeDef = TypedDict(
    "_OptionalListUsersRequestListUsersPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListUsersRequestListUsersPaginateTypeDef(
    _RequiredListUsersRequestListUsersPaginateTypeDef,
    _OptionalListUsersRequestListUsersPaginateTypeDef,
):
    pass


_RequiredListUsersRequestRequestTypeDef = TypedDict(
    "_RequiredListUsersRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalListUsersRequestRequestTypeDef = TypedDict(
    "_OptionalListUsersRequestRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListUsersRequestRequestTypeDef(
    _RequiredListUsersRequestRequestTypeDef, _OptionalListUsersRequestRequestTypeDef
):
    pass


UserTypeDef = TypedDict(
    "UserTypeDef",
    {
        "UserId": str,
        "UserStatus": UserStatusType,
    },
    total=False,
)

MatchedUserTypeDef = TypedDict(
    "MatchedUserTypeDef",
    {
        "UserId": str,
        "UserStatus": UserStatusType,
    },
    total=False,
)

NotificationChannelTypeDef = TypedDict(
    "NotificationChannelTypeDef",
    {
        "SNSTopicArn": str,
        "RoleArn": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

_RequiredPutProjectPolicyRequestRequestTypeDef = TypedDict(
    "_RequiredPutProjectPolicyRequestRequestTypeDef",
    {
        "ProjectArn": str,
        "PolicyName": str,
        "PolicyDocument": str,
    },
)
_OptionalPutProjectPolicyRequestRequestTypeDef = TypedDict(
    "_OptionalPutProjectPolicyRequestRequestTypeDef",
    {
        "PolicyRevisionId": str,
    },
    total=False,
)


class PutProjectPolicyRequestRequestTypeDef(
    _RequiredPutProjectPolicyRequestRequestTypeDef, _OptionalPutProjectPolicyRequestRequestTypeDef
):
    pass


PutProjectPolicyResponseTypeDef = TypedDict(
    "PutProjectPolicyResponseTypeDef",
    {
        "PolicyRevisionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

S3DestinationTypeDef = TypedDict(
    "S3DestinationTypeDef",
    {
        "Bucket": str,
        "KeyPrefix": str,
    },
    total=False,
)

_RequiredSearchFacesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
        "FaceId": str,
    },
)
_OptionalSearchFacesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchFacesRequestRequestTypeDef",
    {
        "MaxFaces": int,
        "FaceMatchThreshold": float,
    },
    total=False,
)


class SearchFacesRequestRequestTypeDef(
    _RequiredSearchFacesRequestRequestTypeDef, _OptionalSearchFacesRequestRequestTypeDef
):
    pass


_RequiredSearchUsersRequestRequestTypeDef = TypedDict(
    "_RequiredSearchUsersRequestRequestTypeDef",
    {
        "CollectionId": str,
    },
)
_OptionalSearchUsersRequestRequestTypeDef = TypedDict(
    "_OptionalSearchUsersRequestRequestTypeDef",
    {
        "UserId": str,
        "FaceId": str,
        "UserMatchThreshold": float,
        "MaxUsers": int,
    },
    total=False,
)


class SearchUsersRequestRequestTypeDef(
    _RequiredSearchUsersRequestRequestTypeDef, _OptionalSearchUsersRequestRequestTypeDef
):
    pass


SearchedFaceTypeDef = TypedDict(
    "SearchedFaceTypeDef",
    {
        "FaceId": str,
    },
    total=False,
)

SearchedUserTypeDef = TypedDict(
    "SearchedUserTypeDef",
    {
        "UserId": str,
    },
    total=False,
)

ShotSegmentTypeDef = TypedDict(
    "ShotSegmentTypeDef",
    {
        "Index": int,
        "Confidence": float,
    },
    total=False,
)

TechnicalCueSegmentTypeDef = TypedDict(
    "TechnicalCueSegmentTypeDef",
    {
        "Type": TechnicalCueTypeType,
        "Confidence": float,
    },
    total=False,
)

StartCelebrityRecognitionResponseTypeDef = TypedDict(
    "StartCelebrityRecognitionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartContentModerationResponseTypeDef = TypedDict(
    "StartContentModerationResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartFaceDetectionResponseTypeDef = TypedDict(
    "StartFaceDetectionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartFaceSearchResponseTypeDef = TypedDict(
    "StartFaceSearchResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartLabelDetectionResponseTypeDef = TypedDict(
    "StartLabelDetectionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartPersonTrackingResponseTypeDef = TypedDict(
    "StartPersonTrackingResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStartProjectVersionRequestRequestTypeDef = TypedDict(
    "_RequiredStartProjectVersionRequestRequestTypeDef",
    {
        "ProjectVersionArn": str,
        "MinInferenceUnits": int,
    },
)
_OptionalStartProjectVersionRequestRequestTypeDef = TypedDict(
    "_OptionalStartProjectVersionRequestRequestTypeDef",
    {
        "MaxInferenceUnits": int,
    },
    total=False,
)


class StartProjectVersionRequestRequestTypeDef(
    _RequiredStartProjectVersionRequestRequestTypeDef,
    _OptionalStartProjectVersionRequestRequestTypeDef,
):
    pass


StartProjectVersionResponseTypeDef = TypedDict(
    "StartProjectVersionResponseTypeDef",
    {
        "Status": ProjectVersionStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartShotDetectionFilterTypeDef = TypedDict(
    "StartShotDetectionFilterTypeDef",
    {
        "MinSegmentConfidence": float,
    },
    total=False,
)

StartSegmentDetectionResponseTypeDef = TypedDict(
    "StartSegmentDetectionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StreamProcessingStopSelectorTypeDef = TypedDict(
    "StreamProcessingStopSelectorTypeDef",
    {
        "MaxDurationInSeconds": int,
    },
    total=False,
)

StartStreamProcessorResponseTypeDef = TypedDict(
    "StartStreamProcessorResponseTypeDef",
    {
        "SessionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartTextDetectionResponseTypeDef = TypedDict(
    "StartTextDetectionResponseTypeDef",
    {
        "JobId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopProjectVersionRequestRequestTypeDef = TypedDict(
    "StopProjectVersionRequestRequestTypeDef",
    {
        "ProjectVersionArn": str,
    },
)

StopProjectVersionResponseTypeDef = TypedDict(
    "StopProjectVersionResponseTypeDef",
    {
        "Status": ProjectVersionStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopStreamProcessorRequestRequestTypeDef = TypedDict(
    "StopStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

AssociateFacesResponseTypeDef = TypedDict(
    "AssociateFacesResponseTypeDef",
    {
        "AssociatedFaces": List[AssociatedFaceTypeDef],
        "UnsuccessfulFaceAssociations": List[UnsuccessfulFaceAssociationTypeDef],
        "UserStatus": UserStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ComparedSourceImageFaceTypeDef = TypedDict(
    "ComparedSourceImageFaceTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
    },
    total=False,
)

FaceTypeDef = TypedDict(
    "FaceTypeDef",
    {
        "FaceId": str,
        "BoundingBox": BoundingBoxTypeDef,
        "ImageId": str,
        "ExternalImageId": str,
        "Confidence": float,
        "IndexFacesModelVersion": str,
        "UserId": str,
    },
    total=False,
)

AuditImageTypeDef = TypedDict(
    "AuditImageTypeDef",
    {
        "Bytes": bytes,
        "S3Object": S3ObjectTypeDef,
        "BoundingBox": BoundingBoxTypeDef,
    },
    total=False,
)

GroundTruthManifestTypeDef = TypedDict(
    "GroundTruthManifestTypeDef",
    {
        "S3Object": S3ObjectTypeDef,
    },
    total=False,
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "Bytes": Union[str, bytes, IO[Any], StreamingBody],
        "S3Object": S3ObjectTypeDef,
    },
    total=False,
)

SummaryTypeDef = TypedDict(
    "SummaryTypeDef",
    {
        "S3Object": S3ObjectTypeDef,
    },
    total=False,
)

VideoTypeDef = TypedDict(
    "VideoTypeDef",
    {
        "S3Object": S3ObjectTypeDef,
    },
    total=False,
)

StartTechnicalCueDetectionFilterTypeDef = TypedDict(
    "StartTechnicalCueDetectionFilterTypeDef",
    {
        "MinSegmentConfidence": float,
        "BlackFrame": BlackFrameTypeDef,
    },
    total=False,
)

GetCelebrityInfoResponseTypeDef = TypedDict(
    "GetCelebrityInfoResponseTypeDef",
    {
        "Urls": List[str],
        "Name": str,
        "KnownGender": KnownGenderTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ComparedFaceTypeDef = TypedDict(
    "ComparedFaceTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
        "Landmarks": List[LandmarkTypeDef],
        "Pose": PoseTypeDef,
        "Quality": ImageQualityTypeDef,
        "Emotions": List[EmotionTypeDef],
        "Smile": SmileTypeDef,
    },
    total=False,
)

StreamProcessorSettingsForUpdateTypeDef = TypedDict(
    "StreamProcessorSettingsForUpdateTypeDef",
    {
        "ConnectedHomeForUpdate": ConnectedHomeSettingsForUpdateTypeDef,
    },
    total=False,
)

ContentModerationDetectionTypeDef = TypedDict(
    "ContentModerationDetectionTypeDef",
    {
        "Timestamp": int,
        "ModerationLabel": ModerationLabelTypeDef,
        "StartTimestampMillis": int,
        "EndTimestampMillis": int,
        "DurationMillis": int,
    },
    total=False,
)

_RequiredCopyProjectVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCopyProjectVersionRequestRequestTypeDef",
    {
        "SourceProjectArn": str,
        "SourceProjectVersionArn": str,
        "DestinationProjectArn": str,
        "VersionName": str,
        "OutputConfig": OutputConfigTypeDef,
    },
)
_OptionalCopyProjectVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCopyProjectVersionRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
        "KmsKeyId": str,
    },
    total=False,
)


class CopyProjectVersionRequestRequestTypeDef(
    _RequiredCopyProjectVersionRequestRequestTypeDef,
    _OptionalCopyProjectVersionRequestRequestTypeDef,
):
    pass


EquipmentDetectionTypeDef = TypedDict(
    "EquipmentDetectionTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
        "Type": ProtectiveEquipmentTypeType,
        "CoversBodyPart": CoversBodyPartTypeDef,
    },
    total=False,
)

CreateFaceLivenessSessionRequestSettingsTypeDef = TypedDict(
    "CreateFaceLivenessSessionRequestSettingsTypeDef",
    {
        "OutputConfig": LivenessOutputConfigTypeDef,
        "AuditImagesLimit": int,
    },
    total=False,
)

UpdateDatasetEntriesRequestRequestTypeDef = TypedDict(
    "UpdateDatasetEntriesRequestRequestTypeDef",
    {
        "DatasetArn": str,
        "Changes": DatasetChangesTypeDef,
    },
)

DatasetDescriptionTypeDef = TypedDict(
    "DatasetDescriptionTypeDef",
    {
        "CreationTimestamp": datetime,
        "LastUpdatedTimestamp": datetime,
        "Status": DatasetStatusType,
        "StatusMessage": str,
        "StatusMessageCode": DatasetStatusMessageCodeType,
        "DatasetStats": DatasetStatsTypeDef,
    },
    total=False,
)

DatasetLabelDescriptionTypeDef = TypedDict(
    "DatasetLabelDescriptionTypeDef",
    {
        "LabelName": str,
        "LabelStats": DatasetLabelStatsTypeDef,
    },
    total=False,
)

ProjectDescriptionTypeDef = TypedDict(
    "ProjectDescriptionTypeDef",
    {
        "ProjectArn": str,
        "CreationTimestamp": datetime,
        "Status": ProjectStatusType,
        "Datasets": List[DatasetMetadataTypeDef],
    },
    total=False,
)

DeleteFacesResponseTypeDef = TypedDict(
    "DeleteFacesResponseTypeDef",
    {
        "DeletedFaces": List[str],
        "UnsuccessfulFaceDeletions": List[UnsuccessfulFaceDeletionTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef = TypedDict(
    "_RequiredDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef = TypedDict(
    "_OptionalDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef",
    {
        "VersionNames": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef(
    _RequiredDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef,
    _OptionalDescribeProjectVersionsRequestProjectVersionRunningWaitTypeDef,
):
    pass


_RequiredDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef = TypedDict(
    "_RequiredDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef",
    {
        "ProjectArn": str,
    },
)
_OptionalDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef = TypedDict(
    "_OptionalDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef",
    {
        "VersionNames": Sequence[str],
        "NextToken": str,
        "MaxResults": int,
        "WaiterConfig": WaiterConfigTypeDef,
    },
    total=False,
)


class DescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef(
    _RequiredDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef,
    _OptionalDescribeProjectVersionsRequestProjectVersionTrainingCompletedWaitTypeDef,
):
    pass


DetectLabelsImageBackgroundTypeDef = TypedDict(
    "DetectLabelsImageBackgroundTypeDef",
    {
        "Quality": DetectLabelsImageQualityTypeDef,
        "DominantColors": List[DominantColorTypeDef],
    },
    total=False,
)

DetectLabelsImageForegroundTypeDef = TypedDict(
    "DetectLabelsImageForegroundTypeDef",
    {
        "Quality": DetectLabelsImageQualityTypeDef,
        "DominantColors": List[DominantColorTypeDef],
    },
    total=False,
)

InstanceTypeDef = TypedDict(
    "InstanceTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
        "DominantColors": List[DominantColorTypeDef],
    },
    total=False,
)

DetectLabelsSettingsTypeDef = TypedDict(
    "DetectLabelsSettingsTypeDef",
    {
        "GeneralLabels": GeneralLabelsSettingsTypeDef,
        "ImageProperties": DetectLabelsImagePropertiesSettingsTypeDef,
    },
    total=False,
)

LabelDetectionSettingsTypeDef = TypedDict(
    "LabelDetectionSettingsTypeDef",
    {
        "GeneralLabels": GeneralLabelsSettingsTypeDef,
    },
    total=False,
)

DetectModerationLabelsResponseTypeDef = TypedDict(
    "DetectModerationLabelsResponseTypeDef",
    {
        "ModerationLabels": List[ModerationLabelTypeDef],
        "ModerationModelVersion": str,
        "HumanLoopActivationOutput": HumanLoopActivationOutputTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DisassociateFacesResponseTypeDef = TypedDict(
    "DisassociateFacesResponseTypeDef",
    {
        "DisassociatedFaces": List[DisassociatedFaceTypeDef],
        "UnsuccessfulFaceDisassociations": List[UnsuccessfulFaceDisassociationTypeDef],
        "UserStatus": UserStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DistributeDatasetEntriesRequestRequestTypeDef = TypedDict(
    "DistributeDatasetEntriesRequestRequestTypeDef",
    {
        "Datasets": Sequence[DistributeDatasetTypeDef],
    },
)

FaceDetailTypeDef = TypedDict(
    "FaceDetailTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "AgeRange": AgeRangeTypeDef,
        "Smile": SmileTypeDef,
        "Eyeglasses": EyeglassesTypeDef,
        "Sunglasses": SunglassesTypeDef,
        "Gender": GenderTypeDef,
        "Beard": BeardTypeDef,
        "Mustache": MustacheTypeDef,
        "EyesOpen": EyeOpenTypeDef,
        "MouthOpen": MouthOpenTypeDef,
        "Emotions": List[EmotionTypeDef],
        "Landmarks": List[LandmarkTypeDef],
        "Pose": PoseTypeDef,
        "Quality": ImageQualityTypeDef,
        "Confidence": float,
        "FaceOccluded": FaceOccludedTypeDef,
        "EyeDirection": EyeDirectionTypeDef,
    },
    total=False,
)

StreamProcessorSettingsTypeDef = TypedDict(
    "StreamProcessorSettingsTypeDef",
    {
        "FaceSearch": FaceSearchSettingsTypeDef,
        "ConnectedHome": ConnectedHomeSettingsTypeDef,
    },
    total=False,
)

GeometryTypeDef = TypedDict(
    "GeometryTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Polygon": List[PointTypeDef],
    },
    total=False,
)

RegionOfInterestTypeDef = TypedDict(
    "RegionOfInterestTypeDef",
    {
        "BoundingBox": BoundingBoxTypeDef,
        "Polygon": Sequence[PointTypeDef],
    },
    total=False,
)

_RequiredHumanLoopConfigTypeDef = TypedDict(
    "_RequiredHumanLoopConfigTypeDef",
    {
        "HumanLoopName": str,
        "FlowDefinitionArn": str,
    },
)
_OptionalHumanLoopConfigTypeDef = TypedDict(
    "_OptionalHumanLoopConfigTypeDef",
    {
        "DataAttributes": HumanLoopDataAttributesTypeDef,
    },
    total=False,
)


class HumanLoopConfigTypeDef(_RequiredHumanLoopConfigTypeDef, _OptionalHumanLoopConfigTypeDef):
    pass


StreamProcessingStartSelectorTypeDef = TypedDict(
    "StreamProcessingStartSelectorTypeDef",
    {
        "KVSStreamStartSelector": KinesisVideoStreamStartSelectorTypeDef,
    },
    total=False,
)

StreamProcessorInputTypeDef = TypedDict(
    "StreamProcessorInputTypeDef",
    {
        "KinesisVideoStream": KinesisVideoStreamTypeDef,
    },
    total=False,
)

ListProjectPoliciesResponseTypeDef = TypedDict(
    "ListProjectPoliciesResponseTypeDef",
    {
        "ProjectPolicies": List[ProjectPolicyTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListStreamProcessorsResponseTypeDef = TypedDict(
    "ListStreamProcessorsResponseTypeDef",
    {
        "NextToken": str,
        "StreamProcessors": List[StreamProcessorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListUsersResponseTypeDef = TypedDict(
    "ListUsersResponseTypeDef",
    {
        "Users": List[UserTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UserMatchTypeDef = TypedDict(
    "UserMatchTypeDef",
    {
        "Similarity": float,
        "User": MatchedUserTypeDef,
    },
    total=False,
)

StreamProcessorOutputTypeDef = TypedDict(
    "StreamProcessorOutputTypeDef",
    {
        "KinesisDataStream": KinesisDataStreamTypeDef,
        "S3Destination": S3DestinationTypeDef,
    },
    total=False,
)

SegmentDetectionTypeDef = TypedDict(
    "SegmentDetectionTypeDef",
    {
        "Type": SegmentTypeType,
        "StartTimestampMillis": int,
        "EndTimestampMillis": int,
        "DurationMillis": int,
        "StartTimecodeSMPTE": str,
        "EndTimecodeSMPTE": str,
        "DurationSMPTE": str,
        "TechnicalCueSegment": TechnicalCueSegmentTypeDef,
        "ShotSegment": ShotSegmentTypeDef,
        "StartFrameNumber": int,
        "EndFrameNumber": int,
        "DurationFrames": int,
    },
    total=False,
)

FaceMatchTypeDef = TypedDict(
    "FaceMatchTypeDef",
    {
        "Similarity": float,
        "Face": FaceTypeDef,
    },
    total=False,
)

ListFacesResponseTypeDef = TypedDict(
    "ListFacesResponseTypeDef",
    {
        "Faces": List[FaceTypeDef],
        "NextToken": str,
        "FaceModelVersion": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFaceLivenessSessionResultsResponseTypeDef = TypedDict(
    "GetFaceLivenessSessionResultsResponseTypeDef",
    {
        "SessionId": str,
        "Status": LivenessSessionStatusType,
        "Confidence": float,
        "ReferenceImage": AuditImageTypeDef,
        "AuditImages": List[AuditImageTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

AssetTypeDef = TypedDict(
    "AssetTypeDef",
    {
        "GroundTruthManifest": GroundTruthManifestTypeDef,
    },
    total=False,
)

DatasetSourceTypeDef = TypedDict(
    "DatasetSourceTypeDef",
    {
        "GroundTruthManifest": GroundTruthManifestTypeDef,
        "DatasetArn": str,
    },
    total=False,
)

_RequiredCompareFacesRequestRequestTypeDef = TypedDict(
    "_RequiredCompareFacesRequestRequestTypeDef",
    {
        "SourceImage": ImageTypeDef,
        "TargetImage": ImageTypeDef,
    },
)
_OptionalCompareFacesRequestRequestTypeDef = TypedDict(
    "_OptionalCompareFacesRequestRequestTypeDef",
    {
        "SimilarityThreshold": float,
        "QualityFilter": QualityFilterType,
    },
    total=False,
)


class CompareFacesRequestRequestTypeDef(
    _RequiredCompareFacesRequestRequestTypeDef, _OptionalCompareFacesRequestRequestTypeDef
):
    pass


_RequiredDetectCustomLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredDetectCustomLabelsRequestRequestTypeDef",
    {
        "ProjectVersionArn": str,
        "Image": ImageTypeDef,
    },
)
_OptionalDetectCustomLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalDetectCustomLabelsRequestRequestTypeDef",
    {
        "MaxResults": int,
        "MinConfidence": float,
    },
    total=False,
)


class DetectCustomLabelsRequestRequestTypeDef(
    _RequiredDetectCustomLabelsRequestRequestTypeDef,
    _OptionalDetectCustomLabelsRequestRequestTypeDef,
):
    pass


_RequiredDetectFacesRequestRequestTypeDef = TypedDict(
    "_RequiredDetectFacesRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectFacesRequestRequestTypeDef = TypedDict(
    "_OptionalDetectFacesRequestRequestTypeDef",
    {
        "Attributes": Sequence[AttributeType],
    },
    total=False,
)


class DetectFacesRequestRequestTypeDef(
    _RequiredDetectFacesRequestRequestTypeDef, _OptionalDetectFacesRequestRequestTypeDef
):
    pass


_RequiredDetectProtectiveEquipmentRequestRequestTypeDef = TypedDict(
    "_RequiredDetectProtectiveEquipmentRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectProtectiveEquipmentRequestRequestTypeDef = TypedDict(
    "_OptionalDetectProtectiveEquipmentRequestRequestTypeDef",
    {
        "SummarizationAttributes": ProtectiveEquipmentSummarizationAttributesTypeDef,
    },
    total=False,
)


class DetectProtectiveEquipmentRequestRequestTypeDef(
    _RequiredDetectProtectiveEquipmentRequestRequestTypeDef,
    _OptionalDetectProtectiveEquipmentRequestRequestTypeDef,
):
    pass


_RequiredIndexFacesRequestRequestTypeDef = TypedDict(
    "_RequiredIndexFacesRequestRequestTypeDef",
    {
        "CollectionId": str,
        "Image": ImageTypeDef,
    },
)
_OptionalIndexFacesRequestRequestTypeDef = TypedDict(
    "_OptionalIndexFacesRequestRequestTypeDef",
    {
        "ExternalImageId": str,
        "DetectionAttributes": Sequence[AttributeType],
        "MaxFaces": int,
        "QualityFilter": QualityFilterType,
    },
    total=False,
)


class IndexFacesRequestRequestTypeDef(
    _RequiredIndexFacesRequestRequestTypeDef, _OptionalIndexFacesRequestRequestTypeDef
):
    pass


RecognizeCelebritiesRequestRequestTypeDef = TypedDict(
    "RecognizeCelebritiesRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)

_RequiredSearchFacesByImageRequestRequestTypeDef = TypedDict(
    "_RequiredSearchFacesByImageRequestRequestTypeDef",
    {
        "CollectionId": str,
        "Image": ImageTypeDef,
    },
)
_OptionalSearchFacesByImageRequestRequestTypeDef = TypedDict(
    "_OptionalSearchFacesByImageRequestRequestTypeDef",
    {
        "MaxFaces": int,
        "FaceMatchThreshold": float,
        "QualityFilter": QualityFilterType,
    },
    total=False,
)


class SearchFacesByImageRequestRequestTypeDef(
    _RequiredSearchFacesByImageRequestRequestTypeDef,
    _OptionalSearchFacesByImageRequestRequestTypeDef,
):
    pass


_RequiredSearchUsersByImageRequestRequestTypeDef = TypedDict(
    "_RequiredSearchUsersByImageRequestRequestTypeDef",
    {
        "CollectionId": str,
        "Image": ImageTypeDef,
    },
)
_OptionalSearchUsersByImageRequestRequestTypeDef = TypedDict(
    "_OptionalSearchUsersByImageRequestRequestTypeDef",
    {
        "UserMatchThreshold": float,
        "MaxUsers": int,
        "QualityFilter": QualityFilterType,
    },
    total=False,
)


class SearchUsersByImageRequestRequestTypeDef(
    _RequiredSearchUsersByImageRequestRequestTypeDef,
    _OptionalSearchUsersByImageRequestRequestTypeDef,
):
    pass


EvaluationResultTypeDef = TypedDict(
    "EvaluationResultTypeDef",
    {
        "F1Score": float,
        "Summary": SummaryTypeDef,
    },
    total=False,
)

_RequiredStartCelebrityRecognitionRequestRequestTypeDef = TypedDict(
    "_RequiredStartCelebrityRecognitionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartCelebrityRecognitionRequestRequestTypeDef = TypedDict(
    "_OptionalStartCelebrityRecognitionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
    },
    total=False,
)


class StartCelebrityRecognitionRequestRequestTypeDef(
    _RequiredStartCelebrityRecognitionRequestRequestTypeDef,
    _OptionalStartCelebrityRecognitionRequestRequestTypeDef,
):
    pass


_RequiredStartContentModerationRequestRequestTypeDef = TypedDict(
    "_RequiredStartContentModerationRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartContentModerationRequestRequestTypeDef = TypedDict(
    "_OptionalStartContentModerationRequestRequestTypeDef",
    {
        "MinConfidence": float,
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
    },
    total=False,
)


class StartContentModerationRequestRequestTypeDef(
    _RequiredStartContentModerationRequestRequestTypeDef,
    _OptionalStartContentModerationRequestRequestTypeDef,
):
    pass


_RequiredStartFaceDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredStartFaceDetectionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartFaceDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalStartFaceDetectionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "FaceAttributes": FaceAttributesType,
        "JobTag": str,
    },
    total=False,
)


class StartFaceDetectionRequestRequestTypeDef(
    _RequiredStartFaceDetectionRequestRequestTypeDef,
    _OptionalStartFaceDetectionRequestRequestTypeDef,
):
    pass


_RequiredStartFaceSearchRequestRequestTypeDef = TypedDict(
    "_RequiredStartFaceSearchRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
        "CollectionId": str,
    },
)
_OptionalStartFaceSearchRequestRequestTypeDef = TypedDict(
    "_OptionalStartFaceSearchRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "FaceMatchThreshold": float,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
    },
    total=False,
)


class StartFaceSearchRequestRequestTypeDef(
    _RequiredStartFaceSearchRequestRequestTypeDef, _OptionalStartFaceSearchRequestRequestTypeDef
):
    pass


_RequiredStartPersonTrackingRequestRequestTypeDef = TypedDict(
    "_RequiredStartPersonTrackingRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartPersonTrackingRequestRequestTypeDef = TypedDict(
    "_OptionalStartPersonTrackingRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
    },
    total=False,
)


class StartPersonTrackingRequestRequestTypeDef(
    _RequiredStartPersonTrackingRequestRequestTypeDef,
    _OptionalStartPersonTrackingRequestRequestTypeDef,
):
    pass


StartSegmentDetectionFiltersTypeDef = TypedDict(
    "StartSegmentDetectionFiltersTypeDef",
    {
        "TechnicalCueFilter": StartTechnicalCueDetectionFilterTypeDef,
        "ShotFilter": StartShotDetectionFilterTypeDef,
    },
    total=False,
)

CelebrityTypeDef = TypedDict(
    "CelebrityTypeDef",
    {
        "Urls": List[str],
        "Name": str,
        "Id": str,
        "Face": ComparedFaceTypeDef,
        "MatchConfidence": float,
        "KnownGender": KnownGenderTypeDef,
    },
    total=False,
)

CompareFacesMatchTypeDef = TypedDict(
    "CompareFacesMatchTypeDef",
    {
        "Similarity": float,
        "Face": ComparedFaceTypeDef,
    },
    total=False,
)

GetContentModerationResponseTypeDef = TypedDict(
    "GetContentModerationResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "ModerationLabels": List[ContentModerationDetectionTypeDef],
        "NextToken": str,
        "ModerationModelVersion": str,
        "JobId": str,
        "Video": VideoTypeDef,
        "JobTag": str,
        "GetRequestMetadata": GetContentModerationRequestMetadataTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ProtectiveEquipmentBodyPartTypeDef = TypedDict(
    "ProtectiveEquipmentBodyPartTypeDef",
    {
        "Name": BodyPartType,
        "Confidence": float,
        "EquipmentDetections": List[EquipmentDetectionTypeDef],
    },
    total=False,
)

CreateFaceLivenessSessionRequestRequestTypeDef = TypedDict(
    "CreateFaceLivenessSessionRequestRequestTypeDef",
    {
        "KmsKeyId": str,
        "Settings": CreateFaceLivenessSessionRequestSettingsTypeDef,
        "ClientRequestToken": str,
    },
    total=False,
)

DescribeDatasetResponseTypeDef = TypedDict(
    "DescribeDatasetResponseTypeDef",
    {
        "DatasetDescription": DatasetDescriptionTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDatasetLabelsResponseTypeDef = TypedDict(
    "ListDatasetLabelsResponseTypeDef",
    {
        "DatasetLabelDescriptions": List[DatasetLabelDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DescribeProjectsResponseTypeDef = TypedDict(
    "DescribeProjectsResponseTypeDef",
    {
        "ProjectDescriptions": List[ProjectDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DetectLabelsImagePropertiesTypeDef = TypedDict(
    "DetectLabelsImagePropertiesTypeDef",
    {
        "Quality": DetectLabelsImageQualityTypeDef,
        "DominantColors": List[DominantColorTypeDef],
        "Foreground": DetectLabelsImageForegroundTypeDef,
        "Background": DetectLabelsImageBackgroundTypeDef,
    },
    total=False,
)

LabelTypeDef = TypedDict(
    "LabelTypeDef",
    {
        "Name": str,
        "Confidence": float,
        "Instances": List[InstanceTypeDef],
        "Parents": List[ParentTypeDef],
        "Aliases": List[LabelAliasTypeDef],
        "Categories": List[LabelCategoryTypeDef],
    },
    total=False,
)

_RequiredDetectLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredDetectLabelsRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalDetectLabelsRequestRequestTypeDef",
    {
        "MaxLabels": int,
        "MinConfidence": float,
        "Features": Sequence[DetectLabelsFeatureNameType],
        "Settings": DetectLabelsSettingsTypeDef,
    },
    total=False,
)


class DetectLabelsRequestRequestTypeDef(
    _RequiredDetectLabelsRequestRequestTypeDef, _OptionalDetectLabelsRequestRequestTypeDef
):
    pass


_RequiredStartLabelDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredStartLabelDetectionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartLabelDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalStartLabelDetectionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "MinConfidence": float,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
        "Features": Sequence[Literal["GENERAL_LABELS"]],
        "Settings": LabelDetectionSettingsTypeDef,
    },
    total=False,
)


class StartLabelDetectionRequestRequestTypeDef(
    _RequiredStartLabelDetectionRequestRequestTypeDef,
    _OptionalStartLabelDetectionRequestRequestTypeDef,
):
    pass


CelebrityDetailTypeDef = TypedDict(
    "CelebrityDetailTypeDef",
    {
        "Urls": List[str],
        "Name": str,
        "Id": str,
        "Confidence": float,
        "BoundingBox": BoundingBoxTypeDef,
        "Face": FaceDetailTypeDef,
        "KnownGender": KnownGenderTypeDef,
    },
    total=False,
)

DetectFacesResponseTypeDef = TypedDict(
    "DetectFacesResponseTypeDef",
    {
        "FaceDetails": List[FaceDetailTypeDef],
        "OrientationCorrection": OrientationCorrectionType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FaceDetectionTypeDef = TypedDict(
    "FaceDetectionTypeDef",
    {
        "Timestamp": int,
        "Face": FaceDetailTypeDef,
    },
    total=False,
)

FaceRecordTypeDef = TypedDict(
    "FaceRecordTypeDef",
    {
        "Face": FaceTypeDef,
        "FaceDetail": FaceDetailTypeDef,
    },
    total=False,
)

PersonDetailTypeDef = TypedDict(
    "PersonDetailTypeDef",
    {
        "Index": int,
        "BoundingBox": BoundingBoxTypeDef,
        "Face": FaceDetailTypeDef,
    },
    total=False,
)

SearchedFaceDetailsTypeDef = TypedDict(
    "SearchedFaceDetailsTypeDef",
    {
        "FaceDetail": FaceDetailTypeDef,
    },
    total=False,
)

UnindexedFaceTypeDef = TypedDict(
    "UnindexedFaceTypeDef",
    {
        "Reasons": List[ReasonType],
        "FaceDetail": FaceDetailTypeDef,
    },
    total=False,
)

UnsearchedFaceTypeDef = TypedDict(
    "UnsearchedFaceTypeDef",
    {
        "FaceDetails": FaceDetailTypeDef,
        "Reasons": List[UnsearchedFaceReasonType],
    },
    total=False,
)

CustomLabelTypeDef = TypedDict(
    "CustomLabelTypeDef",
    {
        "Name": str,
        "Confidence": float,
        "Geometry": GeometryTypeDef,
    },
    total=False,
)

TextDetectionTypeDef = TypedDict(
    "TextDetectionTypeDef",
    {
        "DetectedText": str,
        "Type": TextTypesType,
        "Id": int,
        "ParentId": int,
        "Confidence": float,
        "Geometry": GeometryTypeDef,
    },
    total=False,
)

DetectTextFiltersTypeDef = TypedDict(
    "DetectTextFiltersTypeDef",
    {
        "WordFilter": DetectionFilterTypeDef,
        "RegionsOfInterest": Sequence[RegionOfInterestTypeDef],
    },
    total=False,
)

StartTextDetectionFiltersTypeDef = TypedDict(
    "StartTextDetectionFiltersTypeDef",
    {
        "WordFilter": DetectionFilterTypeDef,
        "RegionsOfInterest": Sequence[RegionOfInterestTypeDef],
    },
    total=False,
)

_RequiredUpdateStreamProcessorRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalUpdateStreamProcessorRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateStreamProcessorRequestRequestTypeDef",
    {
        "SettingsForUpdate": StreamProcessorSettingsForUpdateTypeDef,
        "RegionsOfInterestForUpdate": Sequence[RegionOfInterestTypeDef],
        "DataSharingPreferenceForUpdate": StreamProcessorDataSharingPreferenceTypeDef,
        "ParametersToDelete": Sequence[StreamProcessorParameterToDeleteType],
    },
    total=False,
)


class UpdateStreamProcessorRequestRequestTypeDef(
    _RequiredUpdateStreamProcessorRequestRequestTypeDef,
    _OptionalUpdateStreamProcessorRequestRequestTypeDef,
):
    pass


_RequiredDetectModerationLabelsRequestRequestTypeDef = TypedDict(
    "_RequiredDetectModerationLabelsRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectModerationLabelsRequestRequestTypeDef = TypedDict(
    "_OptionalDetectModerationLabelsRequestRequestTypeDef",
    {
        "MinConfidence": float,
        "HumanLoopConfig": HumanLoopConfigTypeDef,
    },
    total=False,
)


class DetectModerationLabelsRequestRequestTypeDef(
    _RequiredDetectModerationLabelsRequestRequestTypeDef,
    _OptionalDetectModerationLabelsRequestRequestTypeDef,
):
    pass


_RequiredStartStreamProcessorRequestRequestTypeDef = TypedDict(
    "_RequiredStartStreamProcessorRequestRequestTypeDef",
    {
        "Name": str,
    },
)
_OptionalStartStreamProcessorRequestRequestTypeDef = TypedDict(
    "_OptionalStartStreamProcessorRequestRequestTypeDef",
    {
        "StartSelector": StreamProcessingStartSelectorTypeDef,
        "StopSelector": StreamProcessingStopSelectorTypeDef,
    },
    total=False,
)


class StartStreamProcessorRequestRequestTypeDef(
    _RequiredStartStreamProcessorRequestRequestTypeDef,
    _OptionalStartStreamProcessorRequestRequestTypeDef,
):
    pass


SearchUsersResponseTypeDef = TypedDict(
    "SearchUsersResponseTypeDef",
    {
        "UserMatches": List[UserMatchTypeDef],
        "FaceModelVersion": str,
        "SearchedFace": SearchedFaceTypeDef,
        "SearchedUser": SearchedUserTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateStreamProcessorRequestRequestTypeDef = TypedDict(
    "_RequiredCreateStreamProcessorRequestRequestTypeDef",
    {
        "Input": StreamProcessorInputTypeDef,
        "Output": StreamProcessorOutputTypeDef,
        "Name": str,
        "Settings": StreamProcessorSettingsTypeDef,
        "RoleArn": str,
    },
)
_OptionalCreateStreamProcessorRequestRequestTypeDef = TypedDict(
    "_OptionalCreateStreamProcessorRequestRequestTypeDef",
    {
        "Tags": Mapping[str, str],
        "NotificationChannel": StreamProcessorNotificationChannelTypeDef,
        "KmsKeyId": str,
        "RegionsOfInterest": Sequence[RegionOfInterestTypeDef],
        "DataSharingPreference": StreamProcessorDataSharingPreferenceTypeDef,
    },
    total=False,
)


class CreateStreamProcessorRequestRequestTypeDef(
    _RequiredCreateStreamProcessorRequestRequestTypeDef,
    _OptionalCreateStreamProcessorRequestRequestTypeDef,
):
    pass


DescribeStreamProcessorResponseTypeDef = TypedDict(
    "DescribeStreamProcessorResponseTypeDef",
    {
        "Name": str,
        "StreamProcessorArn": str,
        "Status": StreamProcessorStatusType,
        "StatusMessage": str,
        "CreationTimestamp": datetime,
        "LastUpdateTimestamp": datetime,
        "Input": StreamProcessorInputTypeDef,
        "Output": StreamProcessorOutputTypeDef,
        "RoleArn": str,
        "Settings": StreamProcessorSettingsTypeDef,
        "NotificationChannel": StreamProcessorNotificationChannelTypeDef,
        "KmsKeyId": str,
        "RegionsOfInterest": List[RegionOfInterestTypeDef],
        "DataSharingPreference": StreamProcessorDataSharingPreferenceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetSegmentDetectionResponseTypeDef = TypedDict(
    "GetSegmentDetectionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": List[VideoMetadataTypeDef],
        "AudioMetadata": List[AudioMetadataTypeDef],
        "NextToken": str,
        "Segments": List[SegmentDetectionTypeDef],
        "SelectedSegmentTypes": List[SegmentTypeInfoTypeDef],
        "JobId": str,
        "Video": VideoTypeDef,
        "JobTag": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchFacesByImageResponseTypeDef = TypedDict(
    "SearchFacesByImageResponseTypeDef",
    {
        "SearchedFaceBoundingBox": BoundingBoxTypeDef,
        "SearchedFaceConfidence": float,
        "FaceMatches": List[FaceMatchTypeDef],
        "FaceModelVersion": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchFacesResponseTypeDef = TypedDict(
    "SearchFacesResponseTypeDef",
    {
        "SearchedFaceId": str,
        "FaceMatches": List[FaceMatchTypeDef],
        "FaceModelVersion": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TestingDataTypeDef = TypedDict(
    "TestingDataTypeDef",
    {
        "Assets": Sequence[AssetTypeDef],
        "AutoCreate": bool,
    },
    total=False,
)

TrainingDataTypeDef = TypedDict(
    "TrainingDataTypeDef",
    {
        "Assets": Sequence[AssetTypeDef],
    },
    total=False,
)

ValidationDataTypeDef = TypedDict(
    "ValidationDataTypeDef",
    {
        "Assets": List[AssetTypeDef],
    },
    total=False,
)

_RequiredCreateDatasetRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDatasetRequestRequestTypeDef",
    {
        "DatasetType": DatasetTypeType,
        "ProjectArn": str,
    },
)
_OptionalCreateDatasetRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDatasetRequestRequestTypeDef",
    {
        "DatasetSource": DatasetSourceTypeDef,
    },
    total=False,
)


class CreateDatasetRequestRequestTypeDef(
    _RequiredCreateDatasetRequestRequestTypeDef, _OptionalCreateDatasetRequestRequestTypeDef
):
    pass


_RequiredStartSegmentDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredStartSegmentDetectionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
        "SegmentTypes": Sequence[SegmentTypeType],
    },
)
_OptionalStartSegmentDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalStartSegmentDetectionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
        "Filters": StartSegmentDetectionFiltersTypeDef,
    },
    total=False,
)


class StartSegmentDetectionRequestRequestTypeDef(
    _RequiredStartSegmentDetectionRequestRequestTypeDef,
    _OptionalStartSegmentDetectionRequestRequestTypeDef,
):
    pass


RecognizeCelebritiesResponseTypeDef = TypedDict(
    "RecognizeCelebritiesResponseTypeDef",
    {
        "CelebrityFaces": List[CelebrityTypeDef],
        "UnrecognizedFaces": List[ComparedFaceTypeDef],
        "OrientationCorrection": OrientationCorrectionType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CompareFacesResponseTypeDef = TypedDict(
    "CompareFacesResponseTypeDef",
    {
        "SourceImageFace": ComparedSourceImageFaceTypeDef,
        "FaceMatches": List[CompareFacesMatchTypeDef],
        "UnmatchedFaces": List[ComparedFaceTypeDef],
        "SourceImageOrientationCorrection": OrientationCorrectionType,
        "TargetImageOrientationCorrection": OrientationCorrectionType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ProtectiveEquipmentPersonTypeDef = TypedDict(
    "ProtectiveEquipmentPersonTypeDef",
    {
        "BodyParts": List[ProtectiveEquipmentBodyPartTypeDef],
        "BoundingBox": BoundingBoxTypeDef,
        "Confidence": float,
        "Id": int,
    },
    total=False,
)

DetectLabelsResponseTypeDef = TypedDict(
    "DetectLabelsResponseTypeDef",
    {
        "Labels": List[LabelTypeDef],
        "OrientationCorrection": OrientationCorrectionType,
        "LabelModelVersion": str,
        "ImageProperties": DetectLabelsImagePropertiesTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LabelDetectionTypeDef = TypedDict(
    "LabelDetectionTypeDef",
    {
        "Timestamp": int,
        "Label": LabelTypeDef,
        "StartTimestampMillis": int,
        "EndTimestampMillis": int,
        "DurationMillis": int,
    },
    total=False,
)

CelebrityRecognitionTypeDef = TypedDict(
    "CelebrityRecognitionTypeDef",
    {
        "Timestamp": int,
        "Celebrity": CelebrityDetailTypeDef,
    },
    total=False,
)

GetFaceDetectionResponseTypeDef = TypedDict(
    "GetFaceDetectionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Faces": List[FaceDetectionTypeDef],
        "JobId": str,
        "Video": VideoTypeDef,
        "JobTag": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PersonDetectionTypeDef = TypedDict(
    "PersonDetectionTypeDef",
    {
        "Timestamp": int,
        "Person": PersonDetailTypeDef,
    },
    total=False,
)

PersonMatchTypeDef = TypedDict(
    "PersonMatchTypeDef",
    {
        "Timestamp": int,
        "Person": PersonDetailTypeDef,
        "FaceMatches": List[FaceMatchTypeDef],
    },
    total=False,
)

IndexFacesResponseTypeDef = TypedDict(
    "IndexFacesResponseTypeDef",
    {
        "FaceRecords": List[FaceRecordTypeDef],
        "OrientationCorrection": OrientationCorrectionType,
        "FaceModelVersion": str,
        "UnindexedFaces": List[UnindexedFaceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

SearchUsersByImageResponseTypeDef = TypedDict(
    "SearchUsersByImageResponseTypeDef",
    {
        "UserMatches": List[UserMatchTypeDef],
        "FaceModelVersion": str,
        "SearchedFace": SearchedFaceDetailsTypeDef,
        "UnsearchedFaces": List[UnsearchedFaceTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DetectCustomLabelsResponseTypeDef = TypedDict(
    "DetectCustomLabelsResponseTypeDef",
    {
        "CustomLabels": List[CustomLabelTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DetectTextResponseTypeDef = TypedDict(
    "DetectTextResponseTypeDef",
    {
        "TextDetections": List[TextDetectionTypeDef],
        "TextModelVersion": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TextDetectionResultTypeDef = TypedDict(
    "TextDetectionResultTypeDef",
    {
        "Timestamp": int,
        "TextDetection": TextDetectionTypeDef,
    },
    total=False,
)

_RequiredDetectTextRequestRequestTypeDef = TypedDict(
    "_RequiredDetectTextRequestRequestTypeDef",
    {
        "Image": ImageTypeDef,
    },
)
_OptionalDetectTextRequestRequestTypeDef = TypedDict(
    "_OptionalDetectTextRequestRequestTypeDef",
    {
        "Filters": DetectTextFiltersTypeDef,
    },
    total=False,
)


class DetectTextRequestRequestTypeDef(
    _RequiredDetectTextRequestRequestTypeDef, _OptionalDetectTextRequestRequestTypeDef
):
    pass


_RequiredStartTextDetectionRequestRequestTypeDef = TypedDict(
    "_RequiredStartTextDetectionRequestRequestTypeDef",
    {
        "Video": VideoTypeDef,
    },
)
_OptionalStartTextDetectionRequestRequestTypeDef = TypedDict(
    "_OptionalStartTextDetectionRequestRequestTypeDef",
    {
        "ClientRequestToken": str,
        "NotificationChannel": NotificationChannelTypeDef,
        "JobTag": str,
        "Filters": StartTextDetectionFiltersTypeDef,
    },
    total=False,
)


class StartTextDetectionRequestRequestTypeDef(
    _RequiredStartTextDetectionRequestRequestTypeDef,
    _OptionalStartTextDetectionRequestRequestTypeDef,
):
    pass


_RequiredCreateProjectVersionRequestRequestTypeDef = TypedDict(
    "_RequiredCreateProjectVersionRequestRequestTypeDef",
    {
        "ProjectArn": str,
        "VersionName": str,
        "OutputConfig": OutputConfigTypeDef,
    },
)
_OptionalCreateProjectVersionRequestRequestTypeDef = TypedDict(
    "_OptionalCreateProjectVersionRequestRequestTypeDef",
    {
        "TrainingData": TrainingDataTypeDef,
        "TestingData": TestingDataTypeDef,
        "Tags": Mapping[str, str],
        "KmsKeyId": str,
    },
    total=False,
)


class CreateProjectVersionRequestRequestTypeDef(
    _RequiredCreateProjectVersionRequestRequestTypeDef,
    _OptionalCreateProjectVersionRequestRequestTypeDef,
):
    pass


TestingDataResultTypeDef = TypedDict(
    "TestingDataResultTypeDef",
    {
        "Input": TestingDataTypeDef,
        "Output": TestingDataTypeDef,
        "Validation": ValidationDataTypeDef,
    },
    total=False,
)

TrainingDataResultTypeDef = TypedDict(
    "TrainingDataResultTypeDef",
    {
        "Input": TrainingDataTypeDef,
        "Output": TrainingDataTypeDef,
        "Validation": ValidationDataTypeDef,
    },
    total=False,
)

DetectProtectiveEquipmentResponseTypeDef = TypedDict(
    "DetectProtectiveEquipmentResponseTypeDef",
    {
        "ProtectiveEquipmentModelVersion": str,
        "Persons": List[ProtectiveEquipmentPersonTypeDef],
        "Summary": ProtectiveEquipmentSummaryTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLabelDetectionResponseTypeDef = TypedDict(
    "GetLabelDetectionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Labels": List[LabelDetectionTypeDef],
        "LabelModelVersion": str,
        "JobId": str,
        "Video": VideoTypeDef,
        "JobTag": str,
        "GetRequestMetadata": GetLabelDetectionRequestMetadataTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetCelebrityRecognitionResponseTypeDef = TypedDict(
    "GetCelebrityRecognitionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Celebrities": List[CelebrityRecognitionTypeDef],
        "JobId": str,
        "Video": VideoTypeDef,
        "JobTag": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetPersonTrackingResponseTypeDef = TypedDict(
    "GetPersonTrackingResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "NextToken": str,
        "Persons": List[PersonDetectionTypeDef],
        "JobId": str,
        "Video": VideoTypeDef,
        "JobTag": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetFaceSearchResponseTypeDef = TypedDict(
    "GetFaceSearchResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "NextToken": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "Persons": List[PersonMatchTypeDef],
        "JobId": str,
        "Video": VideoTypeDef,
        "JobTag": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetTextDetectionResponseTypeDef = TypedDict(
    "GetTextDetectionResponseTypeDef",
    {
        "JobStatus": VideoJobStatusType,
        "StatusMessage": str,
        "VideoMetadata": VideoMetadataTypeDef,
        "TextDetections": List[TextDetectionResultTypeDef],
        "NextToken": str,
        "TextModelVersion": str,
        "JobId": str,
        "Video": VideoTypeDef,
        "JobTag": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ProjectVersionDescriptionTypeDef = TypedDict(
    "ProjectVersionDescriptionTypeDef",
    {
        "ProjectVersionArn": str,
        "CreationTimestamp": datetime,
        "MinInferenceUnits": int,
        "Status": ProjectVersionStatusType,
        "StatusMessage": str,
        "BillableTrainingTimeInSeconds": int,
        "TrainingEndTimestamp": datetime,
        "OutputConfig": OutputConfigTypeDef,
        "TrainingDataResult": TrainingDataResultTypeDef,
        "TestingDataResult": TestingDataResultTypeDef,
        "EvaluationResult": EvaluationResultTypeDef,
        "ManifestSummary": GroundTruthManifestTypeDef,
        "KmsKeyId": str,
        "MaxInferenceUnits": int,
        "SourceProjectVersionArn": str,
    },
    total=False,
)

DescribeProjectVersionsResponseTypeDef = TypedDict(
    "DescribeProjectVersionsResponseTypeDef",
    {
        "ProjectVersionDescriptions": List[ProjectVersionDescriptionTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
