#!/usr/bin/env python
# Copyright (c) 2018 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


S3_EXTRA_ARGS = {
    'acl': 'ACL',
    'cachecontrol': 'CacheControl',
    'contentdisposition': 'ContentDisposition',
    'contentencoding': 'ContentEncoding',
    'contentlanguage': 'ContentLanguage',
    'contenttype': 'ContentType',
    'expires': 'Expires',
    'grantfullcontrol': 'GrantFullControl',
    'grantread': 'GrantRead',
    'grantreadacp': 'GrantReadACP',
    'grantwriteacp': 'GrantWriteACP',
    'metadata': 'Metadata',
    'requestpayer': 'RequestPayer',
    'serversideencryption': 'ServerSideEncryption',
    'storageclass': 'StorageClass',
    'ssecustomeralgorithm': 'SSECustomerAlgorithm',
    'ssecustomerkey': 'SSECustomerKey',
    'ssecustomerkeymd5': 'SSECustomerKeyMD5',
    'ssekmskeyid': 'SSEKMSKeyId',
    'websiteredirectlocation': 'WebsiteRedirectLocation'
}


def dict_to_s3_extra_args(metadata):
    ret = {}

    for option in metadata:
        mangled = option.translate(None, '-_').lower()
        if mangled in S3_EXTRA_ARGS:
            ret[S3_EXTRA_ARGS[mangled]] = metadata[option]
        else:
            if 'Metadata' not in ret:
                ret['Metadata'] = {}
            ret['Metadata'][option] = metadata[option]

    return ret
