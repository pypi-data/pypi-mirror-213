import requests
import logging
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier

AUTH0_DOMAIN = 'dev-pcpa2zpghqzahboo.eu.auth0.com'
AUTH0_CLIENT_ID = 'KiQTUkMsTKEyCZfie0EPvQSDh4YDMndJ'

class api(object):
    def __init__(self):
        self.url = ""
        self.headers = requests.structures.CaseInsensitiveDict()
        self.headers["Accept"] = "application/json"
        self.headers["Content-Type"] = "application/json"
        self.headers["Accept-Encoding"] = "gzip, deflate, br"
        self.headers["Connection"] = "keep-alive"
        self.headers["Authorization"] = ""

    def is_online(self):
        r = requests.get(self.url)
        if 200 <= r.status_code <= 299:
            return True
        else:
            return False

    def set_access_token(self, _refresh_token, _client_secret, _apiurl="https://api.geoinsight.ai",):
        body = {"grant_type": "refresh_token", "client_id": AUTH0_CLIENT_ID, "refresh_token": _refresh_token, "client_secret": _client_secret}
        r = requests.post('https://{}/oauth/token'.format(AUTH0_DOMAIN), data=body)
        self.url = _apiurl
        if 200 <= r.status_code <= 299 and self.is_online():
            jwks_url = 'https://{}/.well-known/jwks.json'.format(AUTH0_DOMAIN)
            issuer = 'https://{}/'.format(AUTH0_DOMAIN)
            sv = AsymmetricSignatureVerifier(jwks_url)
            tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=AUTH0_CLIENT_ID)
            tv.verify(r.json()['id_token'])
            self.headers["Authorization"] = "Bearer " + '{token}'.format(token=r.json()['access_token'])
            logging.info('Access Token has been set')
        else:
            logging.error('An error occurred: {e}'.format(e=r.json()))
        return

    def atlas_source(self):
        """API endpoint for atlas_source"""
        endpoint = '/atlas_source'
        return requests.get(self.url + endpoint, headers=self.headers)

    def atlas_source_overview(self):
        """API endpoint for atlas_source_overview"""
        endpoint = '/atlas_source_overview'
        return requests.get(self.url + endpoint, headers=self.headers)

    def auth_get_rt(self):
        """API endpoint for auth_get_rt"""
        endpoint = '/auth_get_rt'
        return requests.get(self.url + endpoint, headers=self.headers)

    def destination_source_overview(self):
        """API endpoint for destination_source_overview"""
        endpoint = '/destination_source_overview'
        return requests.get(self.url + endpoint, headers=self.headers)

    def isea3h_data_aoi(self):
        """API endpoint for isea3h_data_aoi"""
        endpoint = '/isea3h_data_aoi'
        return requests.get(self.url + endpoint, headers=self.headers)

    def isea3h_data_destination(self):
        """API endpoint for isea3h_data_destination"""
        endpoint = '/isea3h_data_destination'
        return requests.get(self.url + endpoint, headers=self.headers)

    def isea3h_stats(self):
        """API endpoint for isea3h_stats"""
        endpoint = '/isea3h_stats'
        return requests.get(self.url + endpoint, headers=self.headers)

    def task_common_status_codes(self):
        """API endpoint for task_common_status_codes"""
        endpoint = '/task_common_status_codes'
        return requests.get(self.url + endpoint, headers=self.headers)

    def task_gendggs_overview(self):
        """API endpoint for task_gendggs_overview"""
        endpoint = '/task_gendggs_overview'
        return requests.get(self.url + endpoint, headers=self.headers)

    def task_gendggs_view(self):
        """API endpoint for task_gendggs_view"""
        endpoint = '/task_gendggs_view'
        return requests.get(self.url + endpoint, headers=self.headers)

    def task_logging_view(self):
        """API endpoint for task_logging_view"""
        endpoint = '/task_logging_view'
        return requests.get(self.url + endpoint, headers=self.headers)

    def task_pipeline_overview(self):
        """API endpoint for task_pipeline_overview"""
        endpoint = '/task_pipeline_overview'
        return requests.get(self.url + endpoint, headers=self.headers)

    def task_pipeline_view(self):
        """API endpoint for task_pipeline_view"""
        endpoint = '/task_pipeline_view'
        return requests.get(self.url + endpoint, headers=self.headers)

    def task_ras2dggs_overview(self):
        """API endpoint for task_ras2dggs_overview"""
        endpoint = '/task_ras2dggs_overview'
        return requests.get(self.url + endpoint, headers=self.headers)

    def task_ras2dggs_view(self):
        """API endpoint for task_ras2dggs_view"""
        endpoint = '/task_ras2dggs_view'
        return requests.get(self.url + endpoint, headers=self.headers)

    def atlas_source_delete(self, _id):
        """API endpoint /rpc/atlas_source_delete"""
        endpoint = '/rpc/atlas_source_delete'
        if type(_id) != list:
            logging.error('{}: {} is not {}'.format('_id', _id, 'ARRAY'))
        body = {
                 "_id": _id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def atlas_source_insert(self, _id, _dct_title_s, _gbl_resourceclass_sm, _dct_accessrights_s, _dct_alternative_sm=[], _dct_description_sm=[], _dct_language_sm=[], _dct_creator_sm=[], _dct_publisher_sm=[], _schema_provider_s=None, _gbl_resourcetype_sm=[], _dcat_theme_sm=[], _dcat_keyword_sm=[], _dct_temporal_sm=[], _dct_issued_s=None, _gbl_indexyear_im=None, _gbl_daterange_drsim=[], _dct_spatial_sm=[], _locn_geometry=None, _dcat_bbox=None, _dcat_centroid=None, _pcdm_memberof_sm=[], _dct_ispartof_sm=[], _dct_rights_sm=[], _dct_license_sm=[], _dct_format_s=None, _dct_references_s=None, _dct_identifier_sm=[], _gbl_mdversion_s='Aardvark', _gi_destination=None):
        """API endpoint /rpc/atlas_source_insert"""
        endpoint = '/rpc/atlas_source_insert'
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_dct_title_s) != str and _dct_title_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_title_s', _dct_title_s, 'text'))
        if type(_gbl_resourceclass_sm) != list:
            logging.error('{}: {} is not {}'.format('_gbl_resourceclass_sm', _gbl_resourceclass_sm, 'ARRAY'))
        if type(_dct_accessrights_s) != str and _dct_accessrights_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_accessrights_s', _dct_accessrights_s, 'text'))
        if type(_dct_alternative_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_alternative_sm', _dct_alternative_sm, 'ARRAY'))
        if type(_dct_description_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_description_sm', _dct_description_sm, 'ARRAY'))
        if type(_dct_language_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_language_sm', _dct_language_sm, 'ARRAY'))
        if type(_dct_creator_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_creator_sm', _dct_creator_sm, 'ARRAY'))
        if type(_dct_publisher_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_publisher_sm', _dct_publisher_sm, 'ARRAY'))
        if type(_schema_provider_s) != str and _schema_provider_s is not None:
            logging.error('{}: {} is not {}'.format('_schema_provider_s', _schema_provider_s, 'text'))
        if type(_gbl_resourcetype_sm) != list:
            logging.error('{}: {} is not {}'.format('_gbl_resourcetype_sm', _gbl_resourcetype_sm, 'ARRAY'))
        if type(_dcat_theme_sm) != list:
            logging.error('{}: {} is not {}'.format('_dcat_theme_sm', _dcat_theme_sm, 'ARRAY'))
        if type(_dcat_keyword_sm) != list:
            logging.error('{}: {} is not {}'.format('_dcat_keyword_sm', _dcat_keyword_sm, 'ARRAY'))
        # VALUE CHECK MISSING: _dct_temporal_sm
        if type(_dct_issued_s) != str and _dct_issued_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_issued_s', _dct_issued_s, 'timestamp without time zone'))
        # VALUE CHECK MISSING: _gbl_indexyear_im
        # VALUE CHECK MISSING: _gbl_daterange_drsim
        if type(_dct_spatial_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_spatial_sm', _dct_spatial_sm, 'ARRAY'))
        # VALUE CHECK MISSING: _locn_geometry
        # VALUE CHECK MISSING: _dcat_bbox
        # VALUE CHECK MISSING: _dcat_centroid
        if type(_pcdm_memberof_sm) != list:
            logging.error('{}: {} is not {}'.format('_pcdm_memberof_sm', _pcdm_memberof_sm, 'ARRAY'))
        if type(_dct_ispartof_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_ispartof_sm', _dct_ispartof_sm, 'ARRAY'))
        if type(_dct_rights_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_rights_sm', _dct_rights_sm, 'ARRAY'))
        if type(_dct_license_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_license_sm', _dct_license_sm, 'ARRAY'))
        if type(_dct_format_s) != str and _dct_format_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_format_s', _dct_format_s, 'text'))
        if type(_dct_references_s) != str and _dct_references_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_references_s', _dct_references_s, 'text'))
        if type(_dct_identifier_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_identifier_sm', _dct_identifier_sm, 'ARRAY'))
        if type(_gbl_mdversion_s) != str and _gbl_mdversion_s is not None:
            logging.error('{}: {} is not {}'.format('_gbl_mdversion_s', _gbl_mdversion_s, 'text'))
        if type(_gi_destination) != str and _gi_destination is not None:
            logging.error('{}: {} is not {}'.format('_gi_destination', _gi_destination, 'text'))
        body = {
                 "_id": _id,
                 "_dct_title_s": _dct_title_s,
                 "_gbl_resourceclass_sm": _gbl_resourceclass_sm,
                 "_dct_accessrights_s": _dct_accessrights_s,
                 "_dct_alternative_sm": _dct_alternative_sm,
                 "_dct_description_sm": _dct_description_sm,
                 "_dct_language_sm": _dct_language_sm,
                 "_dct_creator_sm": _dct_creator_sm,
                 "_dct_publisher_sm": _dct_publisher_sm,
                 "_schema_provider_s": _schema_provider_s,
                 "_gbl_resourcetype_sm": _gbl_resourcetype_sm,
                 "_dcat_theme_sm": _dcat_theme_sm,
                 "_dcat_keyword_sm": _dcat_keyword_sm,
                 "_dct_temporal_sm": _dct_temporal_sm,
                 "_dct_issued_s": _dct_issued_s,
                 "_gbl_indexyear_im": _gbl_indexyear_im,
                 "_gbl_daterange_drsim": _gbl_daterange_drsim,
                 "_dct_spatial_sm": _dct_spatial_sm,
                 "_locn_geometry": _locn_geometry,
                 "_dcat_bbox": _dcat_bbox,
                 "_dcat_centroid": _dcat_centroid,
                 "_pcdm_memberof_sm": _pcdm_memberof_sm,
                 "_dct_ispartof_sm": _dct_ispartof_sm,
                 "_dct_rights_sm": _dct_rights_sm,
                 "_dct_license_sm": _dct_license_sm,
                 "_dct_format_s": _dct_format_s,
                 "_dct_references_s": _dct_references_s,
                 "_dct_identifier_sm": _dct_identifier_sm,
                 "_gbl_mdversion_s": _gbl_mdversion_s,
                 "_gi_destination": _gi_destination
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def atlas_source_update(self, _id, _dct_title_s, _dct_alternative_sm, _dct_description_sm, _dct_language_sm, _dct_creator_sm, _dct_publisher_sm, _schema_provider_s, _gbl_resourceclass_sm, _gbl_resourcetype_sm, _dcat_theme_sm, _dcat_keyword_sm, _dct_temporal_sm, _dct_issued_s, _gbl_indexyear_im, _gbl_daterange_drsim, _dct_spatial_sm, _locn_geometry, _dcat_bbox, _dcat_centroid, _pcdm_memberof_sm, _dct_ispartof_sm, _dct_rights_sm, _dct_license_sm, _dct_accessrights_s, _dct_format_s, _dct_references_s, _dct_identifier_sm, _gbl_mdversion_s, _gi_destination):
        """API endpoint /rpc/atlas_source_update"""
        endpoint = '/rpc/atlas_source_update'
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_dct_title_s) != str and _dct_title_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_title_s', _dct_title_s, 'text'))
        if type(_dct_alternative_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_alternative_sm', _dct_alternative_sm, 'ARRAY'))
        if type(_dct_description_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_description_sm', _dct_description_sm, 'ARRAY'))
        if type(_dct_language_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_language_sm', _dct_language_sm, 'ARRAY'))
        if type(_dct_creator_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_creator_sm', _dct_creator_sm, 'ARRAY'))
        if type(_dct_publisher_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_publisher_sm', _dct_publisher_sm, 'ARRAY'))
        if type(_schema_provider_s) != str and _schema_provider_s is not None:
            logging.error('{}: {} is not {}'.format('_schema_provider_s', _schema_provider_s, 'text'))
        if type(_gbl_resourceclass_sm) != list:
            logging.error('{}: {} is not {}'.format('_gbl_resourceclass_sm', _gbl_resourceclass_sm, 'ARRAY'))
        if type(_gbl_resourcetype_sm) != list:
            logging.error('{}: {} is not {}'.format('_gbl_resourcetype_sm', _gbl_resourcetype_sm, 'ARRAY'))
        if type(_dcat_theme_sm) != list:
            logging.error('{}: {} is not {}'.format('_dcat_theme_sm', _dcat_theme_sm, 'ARRAY'))
        if type(_dcat_keyword_sm) != list:
            logging.error('{}: {} is not {}'.format('_dcat_keyword_sm', _dcat_keyword_sm, 'ARRAY'))
        # VALUE CHECK MISSING: _dct_temporal_sm
        if type(_dct_issued_s) != str and _dct_issued_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_issued_s', _dct_issued_s, 'timestamp without time zone'))
        # VALUE CHECK MISSING: _gbl_indexyear_im
        # VALUE CHECK MISSING: _gbl_daterange_drsim
        if type(_dct_spatial_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_spatial_sm', _dct_spatial_sm, 'ARRAY'))
        # VALUE CHECK MISSING: _locn_geometry
        # VALUE CHECK MISSING: _dcat_bbox
        # VALUE CHECK MISSING: _dcat_centroid
        if type(_pcdm_memberof_sm) != list:
            logging.error('{}: {} is not {}'.format('_pcdm_memberof_sm', _pcdm_memberof_sm, 'ARRAY'))
        if type(_dct_ispartof_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_ispartof_sm', _dct_ispartof_sm, 'ARRAY'))
        if type(_dct_rights_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_rights_sm', _dct_rights_sm, 'ARRAY'))
        if type(_dct_license_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_license_sm', _dct_license_sm, 'ARRAY'))
        if type(_dct_accessrights_s) != str and _dct_accessrights_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_accessrights_s', _dct_accessrights_s, 'text'))
        if type(_dct_format_s) != str and _dct_format_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_format_s', _dct_format_s, 'text'))
        if type(_dct_references_s) != str and _dct_references_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_references_s', _dct_references_s, 'text'))
        if type(_dct_identifier_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_identifier_sm', _dct_identifier_sm, 'ARRAY'))
        if type(_gbl_mdversion_s) != str and _gbl_mdversion_s is not None:
            logging.error('{}: {} is not {}'.format('_gbl_mdversion_s', _gbl_mdversion_s, 'text'))
        if type(_gi_destination) != str and _gi_destination is not None:
            logging.error('{}: {} is not {}'.format('_gi_destination', _gi_destination, 'text'))
        body = {
                 "_id": _id,
                 "_dct_title_s": _dct_title_s,
                 "_dct_alternative_sm": _dct_alternative_sm,
                 "_dct_description_sm": _dct_description_sm,
                 "_dct_language_sm": _dct_language_sm,
                 "_dct_creator_sm": _dct_creator_sm,
                 "_dct_publisher_sm": _dct_publisher_sm,
                 "_schema_provider_s": _schema_provider_s,
                 "_gbl_resourceclass_sm": _gbl_resourceclass_sm,
                 "_gbl_resourcetype_sm": _gbl_resourcetype_sm,
                 "_dcat_theme_sm": _dcat_theme_sm,
                 "_dcat_keyword_sm": _dcat_keyword_sm,
                 "_dct_temporal_sm": _dct_temporal_sm,
                 "_dct_issued_s": _dct_issued_s,
                 "_gbl_indexyear_im": _gbl_indexyear_im,
                 "_gbl_daterange_drsim": _gbl_daterange_drsim,
                 "_dct_spatial_sm": _dct_spatial_sm,
                 "_locn_geometry": _locn_geometry,
                 "_dcat_bbox": _dcat_bbox,
                 "_dcat_centroid": _dcat_centroid,
                 "_pcdm_memberof_sm": _pcdm_memberof_sm,
                 "_dct_ispartof_sm": _dct_ispartof_sm,
                 "_dct_rights_sm": _dct_rights_sm,
                 "_dct_license_sm": _dct_license_sm,
                 "_dct_accessrights_s": _dct_accessrights_s,
                 "_dct_format_s": _dct_format_s,
                 "_dct_references_s": _dct_references_s,
                 "_dct_identifier_sm": _dct_identifier_sm,
                 "_gbl_mdversion_s": _gbl_mdversion_s,
                 "_gi_destination": _gi_destination
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def auth_delete_rt(self, _auth0_refresh_token):
        """API endpoint /rpc/auth_delete_rt"""
        endpoint = '/rpc/auth_delete_rt'
        if type(_auth0_refresh_token) != str and _auth0_refresh_token is not None:
            logging.error('{}: {} is not {}'.format('_auth0_refresh_token', _auth0_refresh_token, 'text'))
        body = {
                 "_auth0_refresh_token": _auth0_refresh_token
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def auth_insert_rt(self, _auth0_refresh_token):
        """API endpoint /rpc/auth_insert_rt"""
        endpoint = '/rpc/auth_insert_rt'
        if type(_auth0_refresh_token) != str and _auth0_refresh_token is not None:
            logging.error('{}: {} is not {}'.format('_auth0_refresh_token', _auth0_refresh_token, 'text'))
        body = {
                 "_auth0_refresh_token": _auth0_refresh_token
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def check_aoi_exists(self, _aoi):
        """API endpoint /rpc/check_aoi_exists"""
        endpoint = '/rpc/check_aoi_exists'
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        body = {
                 "_aoi": _aoi
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def check_destination_exists(self, _destination):
        """API endpoint /rpc/check_destination_exists"""
        endpoint = '/rpc/check_destination_exists'
        if type(_destination) != str and _destination is not None:
            logging.error('{}: {} is not {}'.format('_destination', _destination, 'text'))
        body = {
                 "_destination": _destination
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def columns_without_pkey(self, _col_name, _col_pkey):
        """API endpoint /rpc/columns_without_pkey"""
        endpoint = '/rpc/columns_without_pkey'
        if type(_col_name) != list:
            logging.error('{}: {} is not {}'.format('_col_name', _col_name, 'ARRAY'))
        if type(_col_pkey) != list:
            logging.error('{}: {} is not {}'.format('_col_pkey', _col_pkey, 'ARRAY'))
        body = {
                 "_col_name": _col_name,
                 "_col_pkey": _col_pkey
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_aoi(self, _aoi, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_cell_by_aoi"""
        endpoint = '/rpc/isea3h_cell_by_aoi'
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_cell(self, _gid, _gid_res, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_cell_by_cell"""
        endpoint = '/rpc/isea3h_cell_by_cell'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_geojson(self, _res=4, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _limit=10000, _srid=4326):
        """API endpoint /rpc/isea3h_cell_by_geojson"""
        endpoint = '/rpc/isea3h_cell_by_geojson'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'bigint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_geojson": _geojson,
                 "_limit": _limit,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_gid(self, _gid, _res):
        """API endpoint /rpc/isea3h_cell_by_gid"""
        endpoint = '/rpc/isea3h_cell_by_gid'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_gid": _gid,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_point(self, _res, _x, _y, _srid=4326):
        """API endpoint /rpc/isea3h_cell_by_point"""
        endpoint = '/rpc/isea3h_cell_by_point'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_x": _x,
                 "_y": _y,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_aoi(self, _aoi, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_center_by_aoi"""
        endpoint = '/rpc/isea3h_center_by_aoi'
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_cell(self, _gid, _gid_res, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_center_by_cell"""
        endpoint = '/rpc/isea3h_center_by_cell'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_geojson(self, _res=4, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _limit=10000, _srid=4326):
        """API endpoint /rpc/isea3h_center_by_geojson"""
        endpoint = '/rpc/isea3h_center_by_geojson'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'bigint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_geojson": _geojson,
                 "_limit": _limit,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_gid(self, _gid, _res):
        """API endpoint /rpc/isea3h_center_by_gid"""
        endpoint = '/rpc/isea3h_center_by_gid'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_gid": _gid,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_point(self, _res, _y, _x, _srid=4326):
        """API endpoint /rpc/isea3h_center_by_point"""
        endpoint = '/rpc/isea3h_center_by_point'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_y": _y,
                 "_x": _x,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_aoi(self, _aoi, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_children_by_aoi"""
        endpoint = '/rpc/isea3h_children_by_aoi'
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_cell(self, _gid, _gid_res, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_children_by_cell"""
        endpoint = '/rpc/isea3h_children_by_cell'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_geojson(self, _res=4, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _limit=10000, _srid=4326):
        """API endpoint /rpc/isea3h_children_by_geojson"""
        endpoint = '/rpc/isea3h_children_by_geojson'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'bigint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_geojson": _geojson,
                 "_limit": _limit,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_gid(self, _gid, _res):
        """API endpoint /rpc/isea3h_children_by_gid"""
        endpoint = '/rpc/isea3h_children_by_gid'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_gid": _gid,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_point(self, _res, _x, _y, _srid=4326):
        """API endpoint /rpc/isea3h_children_by_point"""
        endpoint = '/rpc/isea3h_children_by_point'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_x": _x,
                 "_y": _y,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_aoi_delete(self, _id):
        """API endpoint /rpc/isea3h_data_aoi_delete"""
        endpoint = '/rpc/isea3h_data_aoi_delete'
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        body = {
                 "_id": _id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_aoi_insert(self, _id, _geojson):
        """API endpoint /rpc/isea3h_data_aoi_insert"""
        endpoint = '/rpc/isea3h_data_aoi_insert'
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        body = {
                 "_id": _id,
                 "_geojson": _geojson
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_aoi_refresh(self, _id):
        """API endpoint /rpc/isea3h_data_aoi_refresh"""
        endpoint = '/rpc/isea3h_data_aoi_refresh'
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        body = {
                 "_id": _id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_aoi_select(self, _id, _res):
        """API endpoint /rpc/isea3h_data_aoi_select"""
        endpoint = '/rpc/isea3h_data_aoi_select'
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        body = {
                 "_id": _id,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_destination_data_upsert(self, _table_name, _values):
        """API endpoint /rpc/isea3h_data_destination_data_upsert"""
        endpoint = '/rpc/isea3h_data_destination_data_upsert'
        if type(_table_name) != str and _table_name is not None:
            logging.error('{}: {} is not {}'.format('_table_name', _table_name, 'text'))
        if type(_values) != dict and _values is not None:
            logging.error('{}: {} is not {}'.format('_values', _values, 'json'))
        body = {
                 "_table_name": _table_name,
                 "_values": _values
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_destination_delete(self, _id):
        """API endpoint /rpc/isea3h_data_destination_delete"""
        endpoint = '/rpc/isea3h_data_destination_delete'
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        body = {
                 "_id": _id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_destination_dense_join_region(self, _destination, _res):
        """API endpoint /rpc/isea3h_data_destination_dense_join_region"""
        endpoint = '/rpc/isea3h_data_destination_dense_join_region'
        if type(_destination) != list:
            logging.error('{}: {} is not {}'.format('_destination', _destination, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_destination": _destination,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_destination_insert(self, _id, _col_name, _col_dtype, _col_pkey=[]):
        """API endpoint /rpc/isea3h_data_destination_insert"""
        endpoint = '/rpc/isea3h_data_destination_insert'
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_col_name) != list:
            logging.error('{}: {} is not {}'.format('_col_name', _col_name, 'ARRAY'))
        if type(_col_dtype) != list:
            logging.error('{}: {} is not {}'.format('_col_dtype', _col_dtype, 'ARRAY'))
        if type(_col_pkey) != list:
            logging.error('{}: {} is not {}'.format('_col_pkey', _col_pkey, 'ARRAY'))
        body = {
                 "_id": _id,
                 "_col_name": _col_name,
                 "_col_dtype": _col_dtype,
                 "_col_pkey": _col_pkey
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_destination_join(self, _destination, _res):
        """API endpoint /rpc/isea3h_data_destination_join"""
        endpoint = '/rpc/isea3h_data_destination_join'
        if type(_destination) != list:
            logging.error('{}: {} is not {}'.format('_destination', _destination, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_destination": _destination,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_destination_join_region(self, _destination, _res):
        """API endpoint /rpc/isea3h_data_destination_join_region"""
        endpoint = '/rpc/isea3h_data_destination_join_region'
        if type(_destination) != list:
            logging.error('{}: {} is not {}'.format('_destination', _destination, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_destination": _destination,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_gid_by_aoi(self, _aoi, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_gid_by_aoi"""
        endpoint = '/rpc/isea3h_gid_by_aoi'
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_gid_by_cell(self, _gid, _gid_res, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_gid_by_cell"""
        endpoint = '/rpc/isea3h_gid_by_cell'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_gid_by_geojson(self, _res=4, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _limit=10000, _srid=4326):
        """API endpoint /rpc/isea3h_gid_by_geojson"""
        endpoint = '/rpc/isea3h_gid_by_geojson'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'bigint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_geojson": _geojson,
                 "_limit": _limit,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_gid_by_point(self, _res, _x, _y, _srid=4326):
        """API endpoint /rpc/isea3h_gid_by_point"""
        endpoint = '/rpc/isea3h_gid_by_point'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_x": _x,
                 "_y": _y,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_insert_cell(self, _values, _res):
        """API endpoint /rpc/isea3h_insert_cell"""
        endpoint = '/rpc/isea3h_insert_cell'
        if type(_values) != dict and _values is not None:
            logging.error('{}: {} is not {}'.format('_values', _values, 'json'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_values": _values,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_aoi(self, _aoi, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_neighbor_by_aoi"""
        endpoint = '/rpc/isea3h_neighbor_by_aoi'
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_cell(self, _gid, _gid_res, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_neighbor_by_cell"""
        endpoint = '/rpc/isea3h_neighbor_by_cell'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_geojson(self, _res=4, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _limit=10000, _srid=4326):
        """API endpoint /rpc/isea3h_neighbor_by_geojson"""
        endpoint = '/rpc/isea3h_neighbor_by_geojson'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'bigint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_geojson": _geojson,
                 "_limit": _limit,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_gid(self, _gid, _res):
        """API endpoint /rpc/isea3h_neighbor_by_gid"""
        endpoint = '/rpc/isea3h_neighbor_by_gid'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_gid": _gid,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_point(self, _res, _x, _y, _srid=4326):
        """API endpoint /rpc/isea3h_neighbor_by_point"""
        endpoint = '/rpc/isea3h_neighbor_by_point'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_x": _x,
                 "_y": _y,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_aoi(self, _aoi, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_region_by_aoi"""
        endpoint = '/rpc/isea3h_region_by_aoi'
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_cell(self, _gid, _gid_res, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_region_by_cell"""
        endpoint = '/rpc/isea3h_region_by_cell'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_cell_ras2dggs(self, _gid, _gid_res, _res=2, _limit=10000):
        """API endpoint /rpc/isea3h_region_by_cell_ras2dggs"""
        endpoint = '/rpc/isea3h_region_by_cell_ras2dggs'
        if type(_gid) != str and _gid is not None:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'text'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_geojson(self, _res=4, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _limit=10000, _srid=4326):
        """API endpoint /rpc/isea3h_region_by_geojson"""
        endpoint = '/rpc/isea3h_region_by_geojson'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'bigint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_geojson": _geojson,
                 "_limit": _limit,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_gid(self, _gid, _res):
        """API endpoint /rpc/isea3h_region_by_gid"""
        endpoint = '/rpc/isea3h_region_by_gid'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_gid": _gid,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_gids(self, _gid, _res):
        """API endpoint /rpc/isea3h_region_by_gids"""
        endpoint = '/rpc/isea3h_region_by_gids'
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        body = {
                 "_gid": _gid,
                 "_res": _res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_point(self, _res, _x, _y, _srid=4326):
        """API endpoint /rpc/isea3h_region_by_point"""
        endpoint = '/rpc/isea3h_region_by_point'
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        body = {
                 "_res": _res,
                 "_x": _x,
                 "_y": _y,
                 "_srid": _srid
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def public_obfuscation_by_point(self, _hf):
        """API endpoint /rpc/public_obfuscation_by_point"""
        endpoint = '/rpc/public_obfuscation_by_point'
        if type(_hf) != list:
            logging.error('{}: {} is not {}'.format('_hf', _hf, 'ARRAY'))
        body = {
                 "_hf": _hf
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_batch(self, _limit=1):
        """API endpoint /rpc/task_gendggs_batch"""
        endpoint = '/rpc/task_gendggs_batch'
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_by_id(self, _task_id):
        """API endpoint /rpc/task_gendggs_by_id"""
        endpoint = '/rpc/task_gendggs_by_id'
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        body = {
                 "_task_id": _task_id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_delete(self, _task_id):
        """API endpoint /rpc/task_gendggs_delete"""
        endpoint = '/rpc/task_gendggs_delete'
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))
        body = {
                 "_task_id": _task_id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_insert(self, _priority, _dggrid_operation, _verbosity, _dggs_res_spec, _clip_subset_type, _input_address_type, _clip_cell_res, _clip_cell_addresses):
        """API endpoint /rpc/task_gendggs_insert"""
        endpoint = '/rpc/task_gendggs_insert'
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_dggrid_operation) != str and _dggrid_operation is not None:
            logging.error('{}: {} is not {}'.format('_dggrid_operation', _dggrid_operation, 'text'))
        if type(_verbosity) != int and _verbosity is not None:
            logging.error('{}: {} is not {}'.format('_verbosity', _verbosity, 'integer'))
        if type(_dggs_res_spec) != list:
            logging.error('{}: {} is not {}'.format('_dggs_res_spec', _dggs_res_spec, 'ARRAY'))
        if type(_clip_subset_type) != str and _clip_subset_type is not None:
            logging.error('{}: {} is not {}'.format('_clip_subset_type', _clip_subset_type, 'text'))
        if type(_input_address_type) != str and _input_address_type is not None:
            logging.error('{}: {} is not {}'.format('_input_address_type', _input_address_type, 'text'))
        if type(_clip_cell_res) != int and _clip_cell_res is not None:
            logging.error('{}: {} is not {}'.format('_clip_cell_res', _clip_cell_res, 'integer'))
        if type(_clip_cell_addresses) != list:
            logging.error('{}: {} is not {}'.format('_clip_cell_addresses', _clip_cell_addresses, 'ARRAY'))
        body = {
                 "_priority": _priority,
                 "_dggrid_operation": _dggrid_operation,
                 "_verbosity": _verbosity,
                 "_dggs_res_spec": _dggs_res_spec,
                 "_clip_subset_type": _clip_subset_type,
                 "_input_address_type": _input_address_type,
                 "_clip_cell_res": _clip_cell_res,
                 "_clip_cell_addresses": _clip_cell_addresses
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_set_status(self, _task_id, _status):
        """API endpoint /rpc/task_gendggs_set_status"""
        endpoint = '/rpc/task_gendggs_set_status'
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))
        if type(_status) != int and _status is not None:
            logging.error('{}: {} is not {}'.format('_status', _status, 'integer'))
        body = {
                 "_task_id": _task_id,
                 "_status": _status
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_update(self, _task_id, _priority, _dggrid_operation, _verbosity, _dggs_res_spec, _clip_subset_type, _input_address_type, _clip_cell_res, _clip_cell_addresses):
        """API endpoint /rpc/task_gendggs_update"""
        endpoint = '/rpc/task_gendggs_update'
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_dggrid_operation) != str and _dggrid_operation is not None:
            logging.error('{}: {} is not {}'.format('_dggrid_operation', _dggrid_operation, 'text'))
        if type(_verbosity) != int and _verbosity is not None:
            logging.error('{}: {} is not {}'.format('_verbosity', _verbosity, 'integer'))
        if type(_dggs_res_spec) != list:
            logging.error('{}: {} is not {}'.format('_dggs_res_spec', _dggs_res_spec, 'ARRAY'))
        if type(_clip_subset_type) != str and _clip_subset_type is not None:
            logging.error('{}: {} is not {}'.format('_clip_subset_type', _clip_subset_type, 'text'))
        if type(_input_address_type) != str and _input_address_type is not None:
            logging.error('{}: {} is not {}'.format('_input_address_type', _input_address_type, 'text'))
        if type(_clip_cell_res) != int and _clip_cell_res is not None:
            logging.error('{}: {} is not {}'.format('_clip_cell_res', _clip_cell_res, 'integer'))
        if type(_clip_cell_addresses) != list:
            logging.error('{}: {} is not {}'.format('_clip_cell_addresses', _clip_cell_addresses, 'ARRAY'))
        body = {
                 "_task_id": _task_id,
                 "_priority": _priority,
                 "_dggrid_operation": _dggrid_operation,
                 "_verbosity": _verbosity,
                 "_dggs_res_spec": _dggs_res_spec,
                 "_clip_subset_type": _clip_subset_type,
                 "_input_address_type": _input_address_type,
                 "_clip_cell_res": _clip_cell_res,
                 "_clip_cell_addresses": _clip_cell_addresses
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_batch(self, _limit=1):
        """API endpoint /rpc/task_pipeline_batch"""
        endpoint = '/rpc/task_pipeline_batch'
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_by_id(self, _task_id):
        """API endpoint /rpc/task_pipeline_by_id"""
        endpoint = '/rpc/task_pipeline_by_id'
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        body = {
                 "_task_id": _task_id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_delete(self, _task_id):
        """API endpoint /rpc/task_pipeline_delete"""
        endpoint = '/rpc/task_pipeline_delete'
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))
        body = {
                 "_task_id": _task_id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_insert(self, _priority, _processor, _pipe, _s3_bucket, _description, _license, _start_date, _end_date, _resolution, _bands, _ts, _ts_interval, _nodata, _format, _value, _comment):
        """API endpoint /rpc/task_pipeline_insert"""
        endpoint = '/rpc/task_pipeline_insert'
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_processor) != str and _processor is not None:
            logging.error('{}: {} is not {}'.format('_processor', _processor, 'text'))
        if type(_pipe) != dict and _pipe is not None:
            logging.error('{}: {} is not {}'.format('_pipe', _pipe, 'json'))
        if type(_s3_bucket) != str and _s3_bucket is not None:
            logging.error('{}: {} is not {}'.format('_s3_bucket', _s3_bucket, 'text'))
        if type(_description) != str and _description is not None:
            logging.error('{}: {} is not {}'.format('_description', _description, 'text'))
        if type(_license) != str and _license is not None:
            logging.error('{}: {} is not {}'.format('_license', _license, 'text'))
        if type(_start_date) != str and _start_date is not None:
            logging.error('{}: {} is not {}'.format('_start_date', _start_date, 'timestamp without time zone'))
        if type(_end_date) != str and _end_date is not None:
            logging.error('{}: {} is not {}'.format('_end_date', _end_date, 'timestamp without time zone'))
        if type(_resolution) != float and _resolution is not None:
            logging.error('{}: {} is not {}'.format('_resolution', _resolution, 'numeric'))
        if type(_bands) != int and _bands is not None:
            logging.error('{}: {} is not {}'.format('_bands', _bands, 'integer'))
        if type(_ts) != bool and _ts is not None:
            logging.error('{}: {} is not {}'.format('_ts', _ts, 'boolean'))
        if type(_ts_interval) != str and _ts_interval is not None:
            logging.error('{}: {} is not {}'.format('_ts_interval', _ts_interval, 'interval'))
        if type(_nodata) != int and _nodata is not None:
            logging.error('{}: {} is not {}'.format('_nodata', _nodata, 'integer'))
        if type(_format) != str and _format is not None:
            logging.error('{}: {} is not {}'.format('_format', _format, 'text'))
        if type(_value) != str and _value is not None:
            logging.error('{}: {} is not {}'.format('_value', _value, 'text'))
        if type(_comment) != str and _comment is not None:
            logging.error('{}: {} is not {}'.format('_comment', _comment, 'text'))
        body = {
                 "_priority": _priority,
                 "_processor": _processor,
                 "_pipe": _pipe,
                 "_s3_bucket": _s3_bucket,
                 "_description": _description,
                 "_license": _license,
                 "_start_date": _start_date,
                 "_end_date": _end_date,
                 "_resolution": _resolution,
                 "_bands": _bands,
                 "_ts": _ts,
                 "_ts_interval": _ts_interval,
                 "_nodata": _nodata,
                 "_format": _format,
                 "_value": _value,
                 "_comment": _comment
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_s3_bucket_update(self, _task_id, _s3_bucket):
        """API endpoint /rpc/task_pipeline_s3_bucket_update"""
        endpoint = '/rpc/task_pipeline_s3_bucket_update'
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        if type(_s3_bucket) != str and _s3_bucket is not None:
            logging.error('{}: {} is not {}'.format('_s3_bucket', _s3_bucket, 'text'))
        body = {
                 "_task_id": _task_id,
                 "_s3_bucket": _s3_bucket
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_set_status(self, _task_id, _status):
        """API endpoint /rpc/task_pipeline_set_status"""
        endpoint = '/rpc/task_pipeline_set_status'
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))
        if type(_status) != int and _status is not None:
            logging.error('{}: {} is not {}'.format('_status', _status, 'integer'))
        body = {
                 "_task_id": _task_id,
                 "_status": _status
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_update(self, _task_id, _priority, _processor, _pipe, _s3_bucket, _description, _license, _start_date, _end_date, _resolution, _bands, _ts, _ts_interval, _nodata, _format, _value, _comment):
        """API endpoint /rpc/task_pipeline_update"""
        endpoint = '/rpc/task_pipeline_update'
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_processor) != str and _processor is not None:
            logging.error('{}: {} is not {}'.format('_processor', _processor, 'text'))
        if type(_pipe) != dict and _pipe is not None:
            logging.error('{}: {} is not {}'.format('_pipe', _pipe, 'json'))
        if type(_s3_bucket) != str and _s3_bucket is not None:
            logging.error('{}: {} is not {}'.format('_s3_bucket', _s3_bucket, 'text'))
        if type(_description) != str and _description is not None:
            logging.error('{}: {} is not {}'.format('_description', _description, 'text'))
        if type(_license) != str and _license is not None:
            logging.error('{}: {} is not {}'.format('_license', _license, 'text'))
        if type(_start_date) != str and _start_date is not None:
            logging.error('{}: {} is not {}'.format('_start_date', _start_date, 'timestamp without time zone'))
        if type(_end_date) != str and _end_date is not None:
            logging.error('{}: {} is not {}'.format('_end_date', _end_date, 'timestamp without time zone'))
        if type(_resolution) != float and _resolution is not None:
            logging.error('{}: {} is not {}'.format('_resolution', _resolution, 'numeric'))
        if type(_bands) != int and _bands is not None:
            logging.error('{}: {} is not {}'.format('_bands', _bands, 'integer'))
        if type(_ts) != bool and _ts is not None:
            logging.error('{}: {} is not {}'.format('_ts', _ts, 'boolean'))
        if type(_ts_interval) != str and _ts_interval is not None:
            logging.error('{}: {} is not {}'.format('_ts_interval', _ts_interval, 'interval'))
        if type(_nodata) != int and _nodata is not None:
            logging.error('{}: {} is not {}'.format('_nodata', _nodata, 'integer'))
        if type(_format) != str and _format is not None:
            logging.error('{}: {} is not {}'.format('_format', _format, 'text'))
        if type(_value) != str and _value is not None:
            logging.error('{}: {} is not {}'.format('_value', _value, 'text'))
        if type(_comment) != str and _comment is not None:
            logging.error('{}: {} is not {}'.format('_comment', _comment, 'text'))
        body = {
                 "_task_id": _task_id,
                 "_priority": _priority,
                 "_processor": _processor,
                 "_pipe": _pipe,
                 "_s3_bucket": _s3_bucket,
                 "_description": _description,
                 "_license": _license,
                 "_start_date": _start_date,
                 "_end_date": _end_date,
                 "_resolution": _resolution,
                 "_bands": _bands,
                 "_ts": _ts,
                 "_ts_interval": _ts_interval,
                 "_nodata": _nodata,
                 "_format": _format,
                 "_value": _value,
                 "_comment": _comment
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_batch(self, _limit=1):
        """API endpoint /rpc/task_ras2dggs_batch"""
        endpoint = '/rpc/task_ras2dggs_batch'
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))
        body = {
                 "_limit": _limit
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_by_id(self, _task_id):
        """API endpoint /rpc/task_ras2dggs_by_id"""
        endpoint = '/rpc/task_ras2dggs_by_id'
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        body = {
                 "_task_id": _task_id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_delete(self, _task_id):
        """API endpoint /rpc/task_ras2dggs_delete"""
        endpoint = '/rpc/task_ras2dggs_delete'
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))
        body = {
                 "_task_id": _task_id
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_insert(self, _priority, _pipeline_id, _statistic, _res, _clip_gid, _clip_gid_res):
        """API endpoint /rpc/task_ras2dggs_insert"""
        endpoint = '/rpc/task_ras2dggs_insert'
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_pipeline_id) != str and _pipeline_id is not None:
            logging.error('{}: {} is not {}'.format('_pipeline_id', _pipeline_id, 'uuid'))
        if type(_statistic) != str and _statistic is not None:
            logging.error('{}: {} is not {}'.format('_statistic', _statistic, 'text'))
        if type(_res) != list:
            logging.error('{}: {} is not {}'.format('_res', _res, 'ARRAY'))
        if type(_clip_gid) != list:
            logging.error('{}: {} is not {}'.format('_clip_gid', _clip_gid, 'ARRAY'))
        if type(_clip_gid_res) != int and _clip_gid_res is not None:
            logging.error('{}: {} is not {}'.format('_clip_gid_res', _clip_gid_res, 'integer'))
        body = {
                 "_priority": _priority,
                 "_pipeline_id": _pipeline_id,
                 "_statistic": _statistic,
                 "_res": _res,
                 "_clip_gid": _clip_gid,
                 "_clip_gid_res": _clip_gid_res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_set_status(self, _task_id, _status):
        """API endpoint /rpc/task_ras2dggs_set_status"""
        endpoint = '/rpc/task_ras2dggs_set_status'
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))
        if type(_status) != int and _status is not None:
            logging.error('{}: {} is not {}'.format('_status', _status, 'integer'))
        body = {
                 "_task_id": _task_id,
                 "_status": _status
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_update(self, _task_id, _priority, _pipeline_id, _statistic, _res, _clip_gid, _clip_gid_res):
        """API endpoint /rpc/task_ras2dggs_update"""
        endpoint = '/rpc/task_ras2dggs_update'
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_pipeline_id) != str and _pipeline_id is not None:
            logging.error('{}: {} is not {}'.format('_pipeline_id', _pipeline_id, 'uuid'))
        if type(_statistic) != str and _statistic is not None:
            logging.error('{}: {} is not {}'.format('_statistic', _statistic, 'text'))
        if type(_res) != list:
            logging.error('{}: {} is not {}'.format('_res', _res, 'ARRAY'))
        if type(_clip_gid) != list:
            logging.error('{}: {} is not {}'.format('_clip_gid', _clip_gid, 'ARRAY'))
        if type(_clip_gid_res) != int and _clip_gid_res is not None:
            logging.error('{}: {} is not {}'.format('_clip_gid_res', _clip_gid_res, 'integer'))
        body = {
                 "_task_id": _task_id,
                 "_priority": _priority,
                 "_pipeline_id": _pipeline_id,
                 "_statistic": _statistic,
                 "_res": _res,
                 "_clip_gid": _clip_gid,
                 "_clip_gid_res": _clip_gid_res
                }
        return requests.post(self.url + endpoint, json=body, headers=self.headers)


