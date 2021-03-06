# PytSite Taxonomy Plugin


## Changelog


### 5.11 (2019-07-13)

Support of `pytsite-9.0`.


### 5.10 (2019-06-04)

Support of `odm_auth-4.0`.


### 5.9 (2019-03-04)

Support of `odm-6.0`.


### 5.8.1 (2019-01-14)

`alias` field existence check fixed.


### 5.8 (2019-01-08)

Support of `odm_ui-7.x`.


### 5.7.1 (2019-01-08)

`widget.TermSelect.minimum_input_length`'s default value set to `1`.


### 5.7 (2019-01-07)

Support of `odm-5.7` and `odm_auth-3.0`.


### 5.6 (2019-01-02)

- `register_model()`'s `menu_title` arg made optional.
- `model.Term`'s indexes and form setup fixed.
- Support of `odm_ui-6.x`.


### 5.5.3 (2018-12-06)

`Term.as_jsonable()`'s error fixed.


### 5.5.2 (2018-11-19)

`Term`'s form widget fixed.


### 5.5.1 (2018-11-14)

Outdated argument usage removed.


### 5.5 (2018-11-14)

Support of `odm_ui-5.x`.


### 5.4 (2018-11-09)

`Term.odm_ui_widget_select_search_entities_title()` implemented.


### 5.3 (2018-11-08)

`Term.odm_ui_widget_select_search_entities()` implemented.


### 5.2 (2018-10-22)

Support of `assetman-5.x` and `widget-4.x`.


### 5.1 (2018-10-12)

Support of `assetman-4.x`.


### 5.0 (2017-10-11)

Support of `pytsite-8.x`, `assetman-3.x`.


### 4.2.1 (2017-09-17)

Typo fixed.


### 4.2 (2017-09-17)

New property `widget.Cloud.link_pattern_field`.


### 4.1 (2017-09-07)

Support of `odm-3.7`.


### 4.0 (2017-08-29)

- Removed API functions: `find_by_title()`, `find_by_alias()`.
- API function `get()` rewritten.


### 3.8.1 (2017-08-28)

Ukrainian terms titles transliteration fixed.


### 3.8 (2018-08-28)

- New widget `TermSelectSearch`.
- Separate 'Taxonomy' section added to admin sidebar's interface.
- Widgets weights fixed.



### 3.7 (2018-08-21)

Support of `widget-2.11`.


### 3.6 (2018-08-09)

`menu_permissions` argument added in `register_model()`.


### 3.5 (2018-08-09)

Support of `odm_auth-1.9`.


### 3.4 (2018-05-13)

Support of `widget-2.0`.


### 3.3 (2018-05-06)

Support of PytSite-7.17.


### 3.2 (2018-04-14)

Support of `odm_ui-3.0`.


### 3.1 (2018-04-07)

Support of `odm-2.0`.


### 3.0.1 (2018-03-20)

Default value of argument `caption_field` of
`widget.TermSelect.__init()__` set to 'title'.


### 3.0 (2018-03-18)

- `create()` API method removed.
- Behaviour of `dispense()` changed.


### 2.9.2 (2018-03-06)

Missing widget's weight definition fixed.


### 2.9.1 (2018-03-01)

Signatures of constructors of some exceptions changed.


### 2.9 (2018-03-01)

- Errors fixed.
- Support for `odm-1.8` added.


### 2.8 (2018-03-01)

- New API function: `get()`.
- New argument `parent` in `create()`.
- New exception: `error.TermNotExist`.


### 2.7 (2018-03-01)

- `error` module added.
- New API function added: `create()`.
- Automatic term's order calculation added.
- ODM indexes refactored.


### 2.6.1 (2018-02-27)

Default ODM UI widget fixed.


### 2.6 (2018-02-27)

Support for entity trees.


### 2.5 (2018-02-12)

- Added `menu_sid` arg to the `register_model()`.
- Admin's section 'Taxonomy' removed.


### 2.4.1 (2018-02-11)

`plugin.json` fixed.


### 2.4 (2018-02-11)

Support for PytSite-7.9.


### 2.3.1 (2018-01-29)

`plugin.json` fixed.


### 2.3 (2018-01-27)

Support for `admin-1.3`.


### 2.2.5 (2017-12-21)

Admin item addition fixed.


### 2.2.4 (2017-12-21)

Init code fixed.


### 2.2.3 (2017-12-21)

Init code fixed.


### 2.2.2 (2017-12-20)

Init code fixed.


### 2.2.1 (2017-12-20)

Init code refactored.


### 2.2 (2017-12-13)

Support for PytSite-7.0.


### 2.1 (2017-12-02)

Support for PytSite-6.1.


### 2.0 (2017-12-25)

Support for PytSite-6.0.


### 1.3 (2017-10-29)

Added fields to `as_jsonable()`'s return value.


### 1.2.1 (2017-10-29)

Fixed images deletion.


### 1.2 (2017-10-29)

Added new field `image` to `model.Term`.


### 1.1 (2017-10-05)

Default sort field of `widget.TermSelect` set to 'order'.


### 1.0.1 (2017-09-18)

`plugin.json` fixed.


### 1.0 (2017-09-13)

Updated to support latest PytSite version 5.0.


### 0.3.3 (2017-08-27)

`plugin.json` updated.


### 0.3.2 (2017-06-15)

Updated to support latest PytSite version 0.99.39.


### 0.3.1 (2017-05-05)

Updated controllers' signatures.


### 0.3 (2017-04-28)

Support for latest PytSite asset management changes.


### 0.2.2 (2017-03-21)

Support latest PytSite `widget`'s changes.


### 0.2.1 (2017-03-18)

Fixed multilingual terms aliases sanitizing.


### 0.2 (2017-03-11)

Added support for terms without links in `widget.Cloud`.


### 0.1.3 (2017-03-03)

Support for latest PytSite router's API function rename.


### 0.1.2 (2017-02-23)

Route name changed.


### 0.1.1 (2017-01-21)

Support latest PytSite `widget`'s changes.


### 0.1 (2017-01-08)

First release.
