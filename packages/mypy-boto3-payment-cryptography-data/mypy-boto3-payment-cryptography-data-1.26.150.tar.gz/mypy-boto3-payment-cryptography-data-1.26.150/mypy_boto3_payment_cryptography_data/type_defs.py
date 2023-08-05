"""
Type annotations for payment-cryptography-data service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_payment_cryptography_data/type_defs/)

Usage::

    ```python
    from mypy_boto3_payment_cryptography_data.type_defs import AmexCardSecurityCodeVersion1TypeDef

    data: AmexCardSecurityCodeVersion1TypeDef = {...}
    ```
"""
import sys
from typing import Any, Dict, Mapping

from .literals import (
    DukptDerivationTypeType,
    DukptEncryptionModeType,
    DukptKeyVariantType,
    EncryptionModeType,
    MacAlgorithmType,
    MajorKeyDerivationModeType,
    PaddingTypeType,
    PinBlockFormatForPinDataType,
    SessionKeyDerivationModeType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AmexCardSecurityCodeVersion1TypeDef",
    "AmexCardSecurityCodeVersion2TypeDef",
    "AsymmetricEncryptionAttributesTypeDef",
    "CardHolderVerificationValueTypeDef",
    "CardVerificationValue1TypeDef",
    "CardVerificationValue2TypeDef",
    "DynamicCardVerificationCodeTypeDef",
    "DynamicCardVerificationValueTypeDef",
    "DiscoverDynamicCardVerificationCodeTypeDef",
    "CryptogramVerificationArpcMethod1TypeDef",
    "CryptogramVerificationArpcMethod2TypeDef",
    "ResponseMetadataTypeDef",
    "DukptAttributesTypeDef",
    "DukptDerivationAttributesTypeDef",
    "DukptEncryptionAttributesTypeDef",
    "SymmetricEncryptionAttributesTypeDef",
    "PinDataTypeDef",
    "Ibm3624NaturalPinTypeDef",
    "Ibm3624PinFromOffsetTypeDef",
    "Ibm3624PinOffsetTypeDef",
    "Ibm3624PinVerificationTypeDef",
    "Ibm3624RandomPinTypeDef",
    "MacAlgorithmDukptTypeDef",
    "SessionKeyDerivationValueTypeDef",
    "VisaPinTypeDef",
    "VisaPinVerificationValueTypeDef",
    "VisaPinVerificationTypeDef",
    "SessionKeyAmexTypeDef",
    "SessionKeyEmv2000TypeDef",
    "SessionKeyEmvCommonTypeDef",
    "SessionKeyMastercardTypeDef",
    "SessionKeyVisaTypeDef",
    "TranslationPinDataIsoFormat034TypeDef",
    "CardGenerationAttributesTypeDef",
    "CardVerificationAttributesTypeDef",
    "CryptogramAuthResponseTypeDef",
    "DecryptDataOutputTypeDef",
    "EncryptDataOutputTypeDef",
    "GenerateCardValidationDataOutputTypeDef",
    "GenerateMacOutputTypeDef",
    "ReEncryptDataOutputTypeDef",
    "TranslatePinDataOutputTypeDef",
    "VerifyAuthRequestCryptogramOutputTypeDef",
    "VerifyCardValidationDataOutputTypeDef",
    "VerifyMacOutputTypeDef",
    "VerifyPinDataOutputTypeDef",
    "EncryptionDecryptionAttributesTypeDef",
    "ReEncryptionAttributesTypeDef",
    "GeneratePinDataOutputTypeDef",
    "MacAlgorithmEmvTypeDef",
    "PinGenerationAttributesTypeDef",
    "PinVerificationAttributesTypeDef",
    "SessionKeyDerivationTypeDef",
    "TranslationIsoFormatsTypeDef",
    "GenerateCardValidationDataInputRequestTypeDef",
    "VerifyCardValidationDataInputRequestTypeDef",
    "DecryptDataInputRequestTypeDef",
    "EncryptDataInputRequestTypeDef",
    "ReEncryptDataInputRequestTypeDef",
    "MacAttributesTypeDef",
    "GeneratePinDataInputRequestTypeDef",
    "VerifyPinDataInputRequestTypeDef",
    "VerifyAuthRequestCryptogramInputRequestTypeDef",
    "TranslatePinDataInputRequestTypeDef",
    "GenerateMacInputRequestTypeDef",
    "VerifyMacInputRequestTypeDef",
)

AmexCardSecurityCodeVersion1TypeDef = TypedDict(
    "AmexCardSecurityCodeVersion1TypeDef",
    {
        "CardExpiryDate": str,
    },
)

AmexCardSecurityCodeVersion2TypeDef = TypedDict(
    "AmexCardSecurityCodeVersion2TypeDef",
    {
        "CardExpiryDate": str,
        "ServiceCode": str,
    },
)

AsymmetricEncryptionAttributesTypeDef = TypedDict(
    "AsymmetricEncryptionAttributesTypeDef",
    {
        "PaddingType": PaddingTypeType,
    },
    total=False,
)

CardHolderVerificationValueTypeDef = TypedDict(
    "CardHolderVerificationValueTypeDef",
    {
        "ApplicationTransactionCounter": str,
        "PanSequenceNumber": str,
        "UnpredictableNumber": str,
    },
)

CardVerificationValue1TypeDef = TypedDict(
    "CardVerificationValue1TypeDef",
    {
        "CardExpiryDate": str,
        "ServiceCode": str,
    },
)

CardVerificationValue2TypeDef = TypedDict(
    "CardVerificationValue2TypeDef",
    {
        "CardExpiryDate": str,
    },
)

DynamicCardVerificationCodeTypeDef = TypedDict(
    "DynamicCardVerificationCodeTypeDef",
    {
        "ApplicationTransactionCounter": str,
        "PanSequenceNumber": str,
        "TrackData": str,
        "UnpredictableNumber": str,
    },
)

DynamicCardVerificationValueTypeDef = TypedDict(
    "DynamicCardVerificationValueTypeDef",
    {
        "ApplicationTransactionCounter": str,
        "CardExpiryDate": str,
        "PanSequenceNumber": str,
        "ServiceCode": str,
    },
)

DiscoverDynamicCardVerificationCodeTypeDef = TypedDict(
    "DiscoverDynamicCardVerificationCodeTypeDef",
    {
        "ApplicationTransactionCounter": str,
        "CardExpiryDate": str,
        "UnpredictableNumber": str,
    },
)

CryptogramVerificationArpcMethod1TypeDef = TypedDict(
    "CryptogramVerificationArpcMethod1TypeDef",
    {
        "AuthResponseCode": str,
    },
)

_RequiredCryptogramVerificationArpcMethod2TypeDef = TypedDict(
    "_RequiredCryptogramVerificationArpcMethod2TypeDef",
    {
        "CardStatusUpdate": str,
    },
)
_OptionalCryptogramVerificationArpcMethod2TypeDef = TypedDict(
    "_OptionalCryptogramVerificationArpcMethod2TypeDef",
    {
        "ProprietaryAuthenticationData": str,
    },
    total=False,
)


class CryptogramVerificationArpcMethod2TypeDef(
    _RequiredCryptogramVerificationArpcMethod2TypeDef,
    _OptionalCryptogramVerificationArpcMethod2TypeDef,
):
    pass


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

DukptAttributesTypeDef = TypedDict(
    "DukptAttributesTypeDef",
    {
        "DukptDerivationType": DukptDerivationTypeType,
        "KeySerialNumber": str,
    },
)

_RequiredDukptDerivationAttributesTypeDef = TypedDict(
    "_RequiredDukptDerivationAttributesTypeDef",
    {
        "KeySerialNumber": str,
    },
)
_OptionalDukptDerivationAttributesTypeDef = TypedDict(
    "_OptionalDukptDerivationAttributesTypeDef",
    {
        "DukptKeyDerivationType": DukptDerivationTypeType,
        "DukptKeyVariant": DukptKeyVariantType,
    },
    total=False,
)


class DukptDerivationAttributesTypeDef(
    _RequiredDukptDerivationAttributesTypeDef, _OptionalDukptDerivationAttributesTypeDef
):
    pass


_RequiredDukptEncryptionAttributesTypeDef = TypedDict(
    "_RequiredDukptEncryptionAttributesTypeDef",
    {
        "KeySerialNumber": str,
    },
)
_OptionalDukptEncryptionAttributesTypeDef = TypedDict(
    "_OptionalDukptEncryptionAttributesTypeDef",
    {
        "DukptKeyDerivationType": DukptDerivationTypeType,
        "DukptKeyVariant": DukptKeyVariantType,
        "InitializationVector": str,
        "Mode": DukptEncryptionModeType,
    },
    total=False,
)


class DukptEncryptionAttributesTypeDef(
    _RequiredDukptEncryptionAttributesTypeDef, _OptionalDukptEncryptionAttributesTypeDef
):
    pass


_RequiredSymmetricEncryptionAttributesTypeDef = TypedDict(
    "_RequiredSymmetricEncryptionAttributesTypeDef",
    {
        "Mode": EncryptionModeType,
    },
)
_OptionalSymmetricEncryptionAttributesTypeDef = TypedDict(
    "_OptionalSymmetricEncryptionAttributesTypeDef",
    {
        "InitializationVector": str,
        "PaddingType": PaddingTypeType,
    },
    total=False,
)


class SymmetricEncryptionAttributesTypeDef(
    _RequiredSymmetricEncryptionAttributesTypeDef, _OptionalSymmetricEncryptionAttributesTypeDef
):
    pass


PinDataTypeDef = TypedDict(
    "PinDataTypeDef",
    {
        "PinOffset": str,
        "VerificationValue": str,
    },
    total=False,
)

Ibm3624NaturalPinTypeDef = TypedDict(
    "Ibm3624NaturalPinTypeDef",
    {
        "DecimalizationTable": str,
        "PinValidationData": str,
        "PinValidationDataPadCharacter": str,
    },
)

Ibm3624PinFromOffsetTypeDef = TypedDict(
    "Ibm3624PinFromOffsetTypeDef",
    {
        "DecimalizationTable": str,
        "PinOffset": str,
        "PinValidationData": str,
        "PinValidationDataPadCharacter": str,
    },
)

Ibm3624PinOffsetTypeDef = TypedDict(
    "Ibm3624PinOffsetTypeDef",
    {
        "DecimalizationTable": str,
        "EncryptedPinBlock": str,
        "PinValidationData": str,
        "PinValidationDataPadCharacter": str,
    },
)

Ibm3624PinVerificationTypeDef = TypedDict(
    "Ibm3624PinVerificationTypeDef",
    {
        "DecimalizationTable": str,
        "PinOffset": str,
        "PinValidationData": str,
        "PinValidationDataPadCharacter": str,
    },
)

Ibm3624RandomPinTypeDef = TypedDict(
    "Ibm3624RandomPinTypeDef",
    {
        "DecimalizationTable": str,
        "PinValidationData": str,
        "PinValidationDataPadCharacter": str,
    },
)

_RequiredMacAlgorithmDukptTypeDef = TypedDict(
    "_RequiredMacAlgorithmDukptTypeDef",
    {
        "DukptKeyVariant": DukptKeyVariantType,
        "KeySerialNumber": str,
    },
)
_OptionalMacAlgorithmDukptTypeDef = TypedDict(
    "_OptionalMacAlgorithmDukptTypeDef",
    {
        "DukptDerivationType": DukptDerivationTypeType,
    },
    total=False,
)


class MacAlgorithmDukptTypeDef(
    _RequiredMacAlgorithmDukptTypeDef, _OptionalMacAlgorithmDukptTypeDef
):
    pass


SessionKeyDerivationValueTypeDef = TypedDict(
    "SessionKeyDerivationValueTypeDef",
    {
        "ApplicationCryptogram": str,
        "ApplicationTransactionCounter": str,
    },
    total=False,
)

VisaPinTypeDef = TypedDict(
    "VisaPinTypeDef",
    {
        "PinVerificationKeyIndex": int,
    },
)

VisaPinVerificationValueTypeDef = TypedDict(
    "VisaPinVerificationValueTypeDef",
    {
        "EncryptedPinBlock": str,
        "PinVerificationKeyIndex": int,
    },
)

VisaPinVerificationTypeDef = TypedDict(
    "VisaPinVerificationTypeDef",
    {
        "PinVerificationKeyIndex": int,
        "VerificationValue": str,
    },
)

SessionKeyAmexTypeDef = TypedDict(
    "SessionKeyAmexTypeDef",
    {
        "PanSequenceNumber": str,
        "PrimaryAccountNumber": str,
    },
)

SessionKeyEmv2000TypeDef = TypedDict(
    "SessionKeyEmv2000TypeDef",
    {
        "ApplicationTransactionCounter": str,
        "PanSequenceNumber": str,
        "PrimaryAccountNumber": str,
    },
)

SessionKeyEmvCommonTypeDef = TypedDict(
    "SessionKeyEmvCommonTypeDef",
    {
        "ApplicationTransactionCounter": str,
        "PanSequenceNumber": str,
        "PrimaryAccountNumber": str,
    },
)

SessionKeyMastercardTypeDef = TypedDict(
    "SessionKeyMastercardTypeDef",
    {
        "ApplicationTransactionCounter": str,
        "PanSequenceNumber": str,
        "PrimaryAccountNumber": str,
        "UnpredictableNumber": str,
    },
)

SessionKeyVisaTypeDef = TypedDict(
    "SessionKeyVisaTypeDef",
    {
        "PanSequenceNumber": str,
        "PrimaryAccountNumber": str,
    },
)

TranslationPinDataIsoFormat034TypeDef = TypedDict(
    "TranslationPinDataIsoFormat034TypeDef",
    {
        "PrimaryAccountNumber": str,
    },
)

CardGenerationAttributesTypeDef = TypedDict(
    "CardGenerationAttributesTypeDef",
    {
        "AmexCardSecurityCodeVersion1": AmexCardSecurityCodeVersion1TypeDef,
        "AmexCardSecurityCodeVersion2": AmexCardSecurityCodeVersion2TypeDef,
        "CardHolderVerificationValue": CardHolderVerificationValueTypeDef,
        "CardVerificationValue1": CardVerificationValue1TypeDef,
        "CardVerificationValue2": CardVerificationValue2TypeDef,
        "DynamicCardVerificationCode": DynamicCardVerificationCodeTypeDef,
        "DynamicCardVerificationValue": DynamicCardVerificationValueTypeDef,
    },
    total=False,
)

CardVerificationAttributesTypeDef = TypedDict(
    "CardVerificationAttributesTypeDef",
    {
        "AmexCardSecurityCodeVersion1": AmexCardSecurityCodeVersion1TypeDef,
        "AmexCardSecurityCodeVersion2": AmexCardSecurityCodeVersion2TypeDef,
        "CardHolderVerificationValue": CardHolderVerificationValueTypeDef,
        "CardVerificationValue1": CardVerificationValue1TypeDef,
        "CardVerificationValue2": CardVerificationValue2TypeDef,
        "DiscoverDynamicCardVerificationCode": DiscoverDynamicCardVerificationCodeTypeDef,
        "DynamicCardVerificationCode": DynamicCardVerificationCodeTypeDef,
        "DynamicCardVerificationValue": DynamicCardVerificationValueTypeDef,
    },
    total=False,
)

CryptogramAuthResponseTypeDef = TypedDict(
    "CryptogramAuthResponseTypeDef",
    {
        "ArpcMethod1": CryptogramVerificationArpcMethod1TypeDef,
        "ArpcMethod2": CryptogramVerificationArpcMethod2TypeDef,
    },
    total=False,
)

DecryptDataOutputTypeDef = TypedDict(
    "DecryptDataOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "PlainText": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EncryptDataOutputTypeDef = TypedDict(
    "EncryptDataOutputTypeDef",
    {
        "CipherText": str,
        "KeyArn": str,
        "KeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateCardValidationDataOutputTypeDef = TypedDict(
    "GenerateCardValidationDataOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "ValidationData": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GenerateMacOutputTypeDef = TypedDict(
    "GenerateMacOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "Mac": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReEncryptDataOutputTypeDef = TypedDict(
    "ReEncryptDataOutputTypeDef",
    {
        "CipherText": str,
        "KeyArn": str,
        "KeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TranslatePinDataOutputTypeDef = TypedDict(
    "TranslatePinDataOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "PinBlock": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyAuthRequestCryptogramOutputTypeDef = TypedDict(
    "VerifyAuthRequestCryptogramOutputTypeDef",
    {
        "AuthResponseValue": str,
        "KeyArn": str,
        "KeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyCardValidationDataOutputTypeDef = TypedDict(
    "VerifyCardValidationDataOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyMacOutputTypeDef = TypedDict(
    "VerifyMacOutputTypeDef",
    {
        "KeyArn": str,
        "KeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

VerifyPinDataOutputTypeDef = TypedDict(
    "VerifyPinDataOutputTypeDef",
    {
        "EncryptionKeyArn": str,
        "EncryptionKeyCheckValue": str,
        "VerificationKeyArn": str,
        "VerificationKeyCheckValue": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

EncryptionDecryptionAttributesTypeDef = TypedDict(
    "EncryptionDecryptionAttributesTypeDef",
    {
        "Asymmetric": AsymmetricEncryptionAttributesTypeDef,
        "Dukpt": DukptEncryptionAttributesTypeDef,
        "Symmetric": SymmetricEncryptionAttributesTypeDef,
    },
    total=False,
)

ReEncryptionAttributesTypeDef = TypedDict(
    "ReEncryptionAttributesTypeDef",
    {
        "Dukpt": DukptEncryptionAttributesTypeDef,
        "Symmetric": SymmetricEncryptionAttributesTypeDef,
    },
    total=False,
)

GeneratePinDataOutputTypeDef = TypedDict(
    "GeneratePinDataOutputTypeDef",
    {
        "EncryptedPinBlock": str,
        "EncryptionKeyArn": str,
        "EncryptionKeyCheckValue": str,
        "GenerationKeyArn": str,
        "GenerationKeyCheckValue": str,
        "PinData": PinDataTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

MacAlgorithmEmvTypeDef = TypedDict(
    "MacAlgorithmEmvTypeDef",
    {
        "MajorKeyDerivationMode": MajorKeyDerivationModeType,
        "PanSequenceNumber": str,
        "PrimaryAccountNumber": str,
        "SessionKeyDerivationMode": SessionKeyDerivationModeType,
        "SessionKeyDerivationValue": SessionKeyDerivationValueTypeDef,
    },
)

PinGenerationAttributesTypeDef = TypedDict(
    "PinGenerationAttributesTypeDef",
    {
        "Ibm3624NaturalPin": Ibm3624NaturalPinTypeDef,
        "Ibm3624PinFromOffset": Ibm3624PinFromOffsetTypeDef,
        "Ibm3624PinOffset": Ibm3624PinOffsetTypeDef,
        "Ibm3624RandomPin": Ibm3624RandomPinTypeDef,
        "VisaPin": VisaPinTypeDef,
        "VisaPinVerificationValue": VisaPinVerificationValueTypeDef,
    },
    total=False,
)

PinVerificationAttributesTypeDef = TypedDict(
    "PinVerificationAttributesTypeDef",
    {
        "Ibm3624Pin": Ibm3624PinVerificationTypeDef,
        "VisaPin": VisaPinVerificationTypeDef,
    },
    total=False,
)

SessionKeyDerivationTypeDef = TypedDict(
    "SessionKeyDerivationTypeDef",
    {
        "Amex": SessionKeyAmexTypeDef,
        "Emv2000": SessionKeyEmv2000TypeDef,
        "EmvCommon": SessionKeyEmvCommonTypeDef,
        "Mastercard": SessionKeyMastercardTypeDef,
        "Visa": SessionKeyVisaTypeDef,
    },
    total=False,
)

TranslationIsoFormatsTypeDef = TypedDict(
    "TranslationIsoFormatsTypeDef",
    {
        "IsoFormat0": TranslationPinDataIsoFormat034TypeDef,
        "IsoFormat1": Mapping[str, Any],
        "IsoFormat3": TranslationPinDataIsoFormat034TypeDef,
        "IsoFormat4": TranslationPinDataIsoFormat034TypeDef,
    },
    total=False,
)

_RequiredGenerateCardValidationDataInputRequestTypeDef = TypedDict(
    "_RequiredGenerateCardValidationDataInputRequestTypeDef",
    {
        "GenerationAttributes": CardGenerationAttributesTypeDef,
        "KeyIdentifier": str,
        "PrimaryAccountNumber": str,
    },
)
_OptionalGenerateCardValidationDataInputRequestTypeDef = TypedDict(
    "_OptionalGenerateCardValidationDataInputRequestTypeDef",
    {
        "ValidationDataLength": int,
    },
    total=False,
)


class GenerateCardValidationDataInputRequestTypeDef(
    _RequiredGenerateCardValidationDataInputRequestTypeDef,
    _OptionalGenerateCardValidationDataInputRequestTypeDef,
):
    pass


VerifyCardValidationDataInputRequestTypeDef = TypedDict(
    "VerifyCardValidationDataInputRequestTypeDef",
    {
        "KeyIdentifier": str,
        "PrimaryAccountNumber": str,
        "ValidationData": str,
        "VerificationAttributes": CardVerificationAttributesTypeDef,
    },
)

DecryptDataInputRequestTypeDef = TypedDict(
    "DecryptDataInputRequestTypeDef",
    {
        "CipherText": str,
        "DecryptionAttributes": EncryptionDecryptionAttributesTypeDef,
        "KeyIdentifier": str,
    },
)

EncryptDataInputRequestTypeDef = TypedDict(
    "EncryptDataInputRequestTypeDef",
    {
        "EncryptionAttributes": EncryptionDecryptionAttributesTypeDef,
        "KeyIdentifier": str,
        "PlainText": str,
    },
)

ReEncryptDataInputRequestTypeDef = TypedDict(
    "ReEncryptDataInputRequestTypeDef",
    {
        "CipherText": str,
        "IncomingEncryptionAttributes": ReEncryptionAttributesTypeDef,
        "IncomingKeyIdentifier": str,
        "OutgoingEncryptionAttributes": ReEncryptionAttributesTypeDef,
        "OutgoingKeyIdentifier": str,
    },
)

MacAttributesTypeDef = TypedDict(
    "MacAttributesTypeDef",
    {
        "Algorithm": MacAlgorithmType,
        "DukptCmac": MacAlgorithmDukptTypeDef,
        "DukptIso9797Algorithm1": MacAlgorithmDukptTypeDef,
        "DukptIso9797Algorithm3": MacAlgorithmDukptTypeDef,
        "EmvMac": MacAlgorithmEmvTypeDef,
    },
    total=False,
)

_RequiredGeneratePinDataInputRequestTypeDef = TypedDict(
    "_RequiredGeneratePinDataInputRequestTypeDef",
    {
        "EncryptionKeyIdentifier": str,
        "GenerationAttributes": PinGenerationAttributesTypeDef,
        "GenerationKeyIdentifier": str,
        "PinBlockFormat": PinBlockFormatForPinDataType,
        "PrimaryAccountNumber": str,
    },
)
_OptionalGeneratePinDataInputRequestTypeDef = TypedDict(
    "_OptionalGeneratePinDataInputRequestTypeDef",
    {
        "PinDataLength": int,
    },
    total=False,
)


class GeneratePinDataInputRequestTypeDef(
    _RequiredGeneratePinDataInputRequestTypeDef, _OptionalGeneratePinDataInputRequestTypeDef
):
    pass


_RequiredVerifyPinDataInputRequestTypeDef = TypedDict(
    "_RequiredVerifyPinDataInputRequestTypeDef",
    {
        "EncryptedPinBlock": str,
        "EncryptionKeyIdentifier": str,
        "PinBlockFormat": PinBlockFormatForPinDataType,
        "PrimaryAccountNumber": str,
        "VerificationAttributes": PinVerificationAttributesTypeDef,
        "VerificationKeyIdentifier": str,
    },
)
_OptionalVerifyPinDataInputRequestTypeDef = TypedDict(
    "_OptionalVerifyPinDataInputRequestTypeDef",
    {
        "DukptAttributes": DukptAttributesTypeDef,
        "PinDataLength": int,
    },
    total=False,
)


class VerifyPinDataInputRequestTypeDef(
    _RequiredVerifyPinDataInputRequestTypeDef, _OptionalVerifyPinDataInputRequestTypeDef
):
    pass


_RequiredVerifyAuthRequestCryptogramInputRequestTypeDef = TypedDict(
    "_RequiredVerifyAuthRequestCryptogramInputRequestTypeDef",
    {
        "AuthRequestCryptogram": str,
        "KeyIdentifier": str,
        "MajorKeyDerivationMode": MajorKeyDerivationModeType,
        "SessionKeyDerivationAttributes": SessionKeyDerivationTypeDef,
        "TransactionData": str,
    },
)
_OptionalVerifyAuthRequestCryptogramInputRequestTypeDef = TypedDict(
    "_OptionalVerifyAuthRequestCryptogramInputRequestTypeDef",
    {
        "AuthResponseAttributes": CryptogramAuthResponseTypeDef,
    },
    total=False,
)


class VerifyAuthRequestCryptogramInputRequestTypeDef(
    _RequiredVerifyAuthRequestCryptogramInputRequestTypeDef,
    _OptionalVerifyAuthRequestCryptogramInputRequestTypeDef,
):
    pass


_RequiredTranslatePinDataInputRequestTypeDef = TypedDict(
    "_RequiredTranslatePinDataInputRequestTypeDef",
    {
        "EncryptedPinBlock": str,
        "IncomingKeyIdentifier": str,
        "IncomingTranslationAttributes": TranslationIsoFormatsTypeDef,
        "OutgoingKeyIdentifier": str,
        "OutgoingTranslationAttributes": TranslationIsoFormatsTypeDef,
    },
)
_OptionalTranslatePinDataInputRequestTypeDef = TypedDict(
    "_OptionalTranslatePinDataInputRequestTypeDef",
    {
        "IncomingDukptAttributes": DukptDerivationAttributesTypeDef,
        "OutgoingDukptAttributes": DukptDerivationAttributesTypeDef,
    },
    total=False,
)


class TranslatePinDataInputRequestTypeDef(
    _RequiredTranslatePinDataInputRequestTypeDef, _OptionalTranslatePinDataInputRequestTypeDef
):
    pass


_RequiredGenerateMacInputRequestTypeDef = TypedDict(
    "_RequiredGenerateMacInputRequestTypeDef",
    {
        "GenerationAttributes": MacAttributesTypeDef,
        "KeyIdentifier": str,
        "MessageData": str,
    },
)
_OptionalGenerateMacInputRequestTypeDef = TypedDict(
    "_OptionalGenerateMacInputRequestTypeDef",
    {
        "MacLength": int,
    },
    total=False,
)


class GenerateMacInputRequestTypeDef(
    _RequiredGenerateMacInputRequestTypeDef, _OptionalGenerateMacInputRequestTypeDef
):
    pass


_RequiredVerifyMacInputRequestTypeDef = TypedDict(
    "_RequiredVerifyMacInputRequestTypeDef",
    {
        "KeyIdentifier": str,
        "Mac": str,
        "MessageData": str,
        "VerificationAttributes": MacAttributesTypeDef,
    },
)
_OptionalVerifyMacInputRequestTypeDef = TypedDict(
    "_OptionalVerifyMacInputRequestTypeDef",
    {
        "MacLength": int,
    },
    total=False,
)


class VerifyMacInputRequestTypeDef(
    _RequiredVerifyMacInputRequestTypeDef, _OptionalVerifyMacInputRequestTypeDef
):
    pass
