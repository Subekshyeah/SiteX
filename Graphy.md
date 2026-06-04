# Graphy Codebase Analysis

## Project: d:\projects\SiteX

### File Structure Summary
- Total Files: 4630
- Total Directories: 441
- File Extensions: .sh: 1, .1: 1, .md: 9, .json: 199, .txt: 24, .geojson: 10, .html: 6, .png: 1, .db: 6, .py: 2343, .csv: 110, .db-journal: 1, .ipynb: 6, .pkl: 9, .zip: 1, .cfg: 2, .csh: 1, .fish: 1, .ps1: 1, .13: 2, .gz: 4, .pyi: 304, .typed: 15, .pxd: 7, .c: 6, .h: 27, .f90: 61, .f: 24, .pyf: 7, .inc: 1, .f95: 1, .template: 1, .so: 64, .npy: 5, .npz: 2, .rst: 1, .a: 2, .pyx: 4, .build: 3, .ini: 3, .pc: 1, .cpp: 1, .fits: 1, .0: 2, .toml: 1, .tpl: 7, .pem: 1, .exe: 7, .APACHE: 1, .BSD: 1, .tab: 8, .zi: 2, .dll: 26, .pdf: 2, .js: 3, .tsbuildinfo: 1, .ts: 2, .jpg: 11, .svg: 3, .css: 3, .tsx: 11

### Directory Tree
```
  ├── backend
   │  ├── app
   │  │  ├── api
   │  │  │  ├── endpoints
   │  │  │  │  ├── analysis.py
   │  │  │  │  ├── cafe_processing.py
   │  │  │  │  ├── explain.py
   │  │  │  │  ├── pois.py
   │  │  │  │  ├── predict.py
   │  │  │  │  ├── road_types.py
   │  │  │  │  └── __init__.py
   │  │  │  └── __init__.py
   │  │  ├── core
   │  │  │  ├── config.py
   │  │  │  └── __init__.py
   │  │  ├── lib
   │  │  │  ├── gnn
   │  │  │  │  ├── edge_features.py
   │  │  │  │  ├── graph_builder.py
   │  │  │  │  ├── node_features.py
   │  │  │  │  └── __init__.py
   │  │  │  ├── road_network.py
   │  │  │  ├── road_type_network.py
   │  │  │  └── __init__.py
   │  │  ├── main.py
   │  │  ├── schemas
   │  │  │  ├── cafe.py
   │  │  │  └── __init__.py
   │  │  ├── services
   │  │  │  ├── data_preprocessor.py
   │  │  │  ├── prediction_service.py
   │  │  │  ├── site_analysis_service.py
   │  │  │  └── __init__.py
   │  │  └── __init__.py
   │  ├── data
   │  │  └── external
   │  │    └── cafes_all_data.csv
   │  ├── DataEngineering
   │  │  ├── CSV_Reference
   │  │  │  ├── banks.csv
   │  │  │  ├── banks_all_data.csv
   │  │  │  ├── cafes.csv
   │  │  │  ├── cafes_all_data.csv
   │  │  │  ├── education.csv
   │  │  │  ├── education_all_data.csv
   │  │  │  ├── final
   │  │  │  │  ├── banks_final.csv
   │  │  │  │  ├── cafe_final.csv
   │  │  │  │  ├── education_final.csv
   │  │  │  │  ├── health_final.csv
   │  │  │  │  ├── master_cafes_minimal.csv
   │  │  │  │  ├── master_cafe_path_minimal.csv
   │  │  │  │  ├── other_final.csv
   │  │  │  │  ├── temples_final.csv
   │  │  │  │  └── test_set_cafes.csv
   │  │  │  ├── health.csv
   │  │  │  ├── health_all_data.csv
   │  │  │  ├── master_cafes_metrics.csv
   │  │  │  ├── other.csv
   │  │  │  ├── other_all_data.csv
   │  │  │  ├── temples.csv
   │  │  │  └── temples_all_data.csv
   │  │  ├── data_legit
   │  │  │  └── data_legit
   │  │  │    ├── by_category
   │  │  │     │  ├── bank
   │  │  │     │  │  ├── Bank.json
   │  │  │     │  │  ├── Cooperative bank.json
   │  │  │     │  │  ├── csv
   │  │  │     │  │  │  ├── compact_summary.csv
   │  │  │     │  │  │  └── flattened_all_fields.csv
   │  │  │     │  │  └── flatfetch.py
   │  │  │     │  ├── education
   │  │  │     │  │  ├── After school program.json
   │  │  │     │  │  ├── Art school.json
   │  │  │     │  │  ├── Bartending school.json
   │  │  │     │  │  ├── Boarding school.json
   │  │  │     │  │  ├── Business school.json
   │  │  │     │  │  ├── Children_s library.json
   │  │  │     │  │  ├── Chinese language school.json
   │  │  │     │  │  ├── College.json
   │  │  │     │  │  ├── Combined primary and secondary school.json
   │  │  │     │  │  ├── Community college.json
   │  │  │     │  │  ├── Computer training school.json
   │  │  │     │  │  ├── csv
   │  │  │     │  │  │  ├── compact_summary.csv
   │  │  │     │  │  │  └── flattened_all_fields.csv
   │  │  │     │  │  ├── Dance school.json
   │  │  │     │  │  ├── Drawing lessons.json
   │  │  │     │  │  ├── Drivers license training school.json
   │  │  │     │  │  ├── Driving school.json
   │  │  │     │  │  ├── Education center.json
   │  │  │     │  │  ├── Educational institution.json
   │  │  │     │  │  ├── Elementary school.json
   │  │  │     │  │  ├── English language school.json
   │  │  │     │  │  ├── Farm school.json
   │  │  │     │  │  ├── flatfetch.py
   │  │  │     │  │  ├── General education school.json
   │  │  │     │  │  ├── German language school.json
   │  │  │     │  │  ├── Government school.json
   │  │  │     │  │  ├── High school.json
   │  │  │     │  │  ├── Higher secondary school.json
   │  │  │     │  │  ├── International school.json
   │  │  │     │  │  ├── Language school.json
   │  │  │     │  │  ├── Library.json
   │  │  │     │  │  ├── Middle school.json
   │  │  │     │  │  ├── Montessori preschool.json
   │  │  │     │  │  ├── Montessori school.json
   │  │  │     │  │  ├── Music school.json
   │  │  │     │  │  ├── Preschool.json
   │  │  │     │  │  ├── Primary school.json
   │  │  │     │  │  ├── Private educational institution.json
   │  │  │     │  │  ├── School center.json
   │  │  │     │  │  ├── School house.json
   │  │  │     │  │  ├── School supply store.json
   │  │  │     │  │  ├── Secondary school.json
   │  │  │     │  │  ├── Special education school.json
   │  │  │     │  │  ├── Taekwondo school.json
   │  │  │     │  │  ├── Technical school.json
   │  │  │     │  │  ├── Training center.json
   │  │  │     │  │  ├── University.json
   │  │  │     │  │  └── Vocational school.json
   │  │  │     │  ├── health
   │  │  │     │  │  ├── Acupuncture clinic.json
   │  │  │     │  │  ├── Animal hospital.json
   │  │  │     │  │  ├── Ayurvedic clinic.json
   │  │  │     │  │  ├── Blood bank.json
   │  │  │     │  │  ├── Cancer treatment center.json
   │  │  │     │  │  ├── Child health care center.json
   │  │  │     │  │  ├── Community health center.json
   │  │  │     │  │  ├── csv
   │  │  │     │  │  │  ├── compact_summary.csv
   │  │  │     │  │  │  └── flattened_all_fields.csv
   │  │  │     │  │  ├── Dental clinic.json
   │  │  │     │  │  ├── Dentist.json
   │  │  │     │  │  ├── Faculty of pharmacy.json
   │  │  │     │  │  ├── flatfetch.py
   │  │  │     │  │  ├── General hospital.json
   │  │  │     │  │  ├── Government hospital.json
   │  │  │     │  │  ├── Health and beauty shop.json
   │  │  │     │  │  ├── Health consultant.json
   │  │  │     │  │  ├── Health food store.json
   │  │  │     │  │  ├── Health insurance agency.json
   │  │  │     │  │  ├── Home health care service.json
   │  │  │     │  │  ├── Hospital department.json
   │  │  │     │  │  ├── Hospital equipment and supplies.json
   │  │  │     │  │  ├── Hospital.json
   │  │  │     │  │  ├── Hospitality and tourism school.json
   │  │  │     │  │  ├── Medical clinic.json
   │  │  │     │  │  ├── Mental health service.json
   │  │  │     │  │  ├── Naturopathic practitioner.json
   │  │  │     │  │  ├── Occupational health service.json
   │  │  │     │  │  ├── Orthopedic clinic.json
   │  │  │     │  │  ├── Pain management physician.json
   │  │  │     │  │  ├── Pharmacy.json
   │  │  │     │  │  ├── Physical therapy clinic.json
   │  │  │     │  │  ├── Private hospital.json
   │  │  │     │  │  ├── Public library.json
   │  │  │     │  │  ├── Savings bank.json
   │  │  │     │  │  ├── Self service health station.json
   │  │  │     │  │  ├── Software company.json
   │  │  │     │  │  ├── Ticket office.json
   │  │  │     │  │  ├── Tour operator.json
   │  │  │     │  │  ├── Traffic police station.json
   │  │  │     │  │  ├── Travel agency.json
   │  │  │     │  │  ├── Veterinarian.json
   │  │  │     │  │  └── Veterinary pharmacy.json
   │  │  │     │  ├── other
   │  │  │     │  │  ├── Adventure sports center.json
   │  │  │     │  │  ├── Athletic park.json
   │  │  │     │  │  ├── Banquet hall.json
   │  │  │     │  │  ├── Beauty salon.json
   │  │  │     │  │  ├── Beauty school.json
   │  │  │     │  │  ├── Boxing gym.json
   │  │  │     │  │  ├── Business park.json
   │  │  │     │  │  ├── City government office.json
   │  │  │     │  │  ├── Community garden.json
   │  │  │     │  │  ├── Corporate office.json
   │  │  │     │  │  ├── csv
   │  │  │     │  │  │  ├── compact_summary.csv
   │  │  │     │  │  │  └── flattened_all_fields.csv
   │  │  │     │  │  ├── District office.json
   │  │  │     │  │  ├── Federal government office.json
   │  │  │     │  │  ├── Financial institution.json
   │  │  │     │  │  ├── flatfetch.py
   │  │  │     │  │  ├── Food bank.json
   │  │  │     │  │  ├── Garden.json
   │  │  │     │  │  ├── Government economic program.json
   │  │  │     │  │  ├── Government office.json
   │  │  │     │  │  ├── Government.json
   │  │  │     │  │  ├── Gym.json
   │  │  │     │  │  ├── Local government office.json
   │  │  │     │  │  ├── Memorial park.json
   │  │  │     │  │  ├── Military school.json
   │  │  │     │  │  ├── Mobile home park.json
   │  │  │     │  │  ├── Muay Thai boxing gym.json
   │  │  │     │  │  ├── Office supply store.json
   │  │  │     │  │  ├── Office.json
   │  │  │     │  │  ├── Park _ ride.json
   │  │  │     │  │  ├── Park.json
   │  │  │     │  │  ├── Photography studio.json
   │  │  │     │  │  ├── Plaza.json
   │  │  │     │  │  ├── Political party office.json
   │  │  │     │  │  ├── Post office.json
   │  │  │     │  │  ├── State government office.json
   │  │  │     │  │  └── Water park.json
   │  │  │     │  └── temples_attraction
   │  │  │     │    ├── Buddhist temple.json
   │  │  │     │    ├── csv
   │  │  │     │     │  ├── compact_summary.csv
   │  │  │     │     │  └── flattened_all_fields.csv
   │  │  │     │    ├── flatfetch.py
   │  │  │     │    ├── Hindu temple.json
   │  │  │     │    └── Tourist attraction.json
   │  │  │    ├── comp
   │  │  │     │  ├── bhaktapur_cafes_compact.csv
   │  │  │     │  ├── bhaktapur_cafes_flattened.csv
   │  │  │     │  ├── bh_no_dupli.csv
   │  │  │     │  ├── by_category
   │  │  │     │  │  ├── Adventure sports center.json
   │  │  │     │  │  ├── American restaurant.json
   │  │  │     │  │  ├── Asian restaurant.json
   │  │  │     │  │  ├── Assamese restaurant.json
   │  │  │     │  │  ├── Bakery.json
   │  │  │     │  │  ├── Banquet hall.json
   │  │  │     │  │  ├── Bar.json
   │  │  │     │  │  ├── Barbecue restaurant.json
   │  │  │     │  │  ├── Bed _ breakfast.json
   │  │  │     │  │  ├── Biryani restaurant.json
   │  │  │     │  │  ├── Breakfast restaurant.json
   │  │  │     │  │  ├── Brunch restaurant.json
   │  │  │     │  │  ├── Bubble tea store.json
   │  │  │     │  │  ├── Cafe.json
   │  │  │     │  │  ├── Candy store.json
   │  │  │     │  │  ├── Chicken restaurant.json
   │  │  │     │  │  ├── Chicken wings restaurant.json
   │  │  │     │  │  ├── Children_s cafe.json
   │  │  │     │  │  ├── Chinese noodle restaurant.json
   │  │  │     │  │  ├── Chinese restaurant.json
   │  │  │     │  │  ├── Coffee shop.json
   │  │  │     │  │  ├── Coffee store.json
   │  │  │     │  │  ├── Cottage rental.json
   │  │  │     │  │  ├── Dairy store.json
   │  │  │     │  │  ├── Dessert restaurant.json
   │  │  │     │  │  ├── Dessert shop.json
   │  │  │     │  │  ├── Dog cafe.json
   │  │  │     │  │  ├── Door manufacturer.json
   │  │  │     │  │  ├── Dumpling restaurant.json
   │  │  │     │  │  ├── Espresso bar.json
   │  │  │     │  │  ├── Family restaurant.json
   │  │  │     │  │  ├── Fast food restaurant.json
   │  │  │     │  │  ├── Hamburger restaurant.json
   │  │  │     │  │  ├── Hong Kong style fast food restaurant.json
   │  │  │     │  │  ├── Ice cream shop.json
   │  │  │     │  │  ├── Indian restaurant.json
   │  │  │     │  │  ├── Internet cafe.json
   │  │  │     │  │  ├── Korean restaurant.json
   │  │  │     │  │  ├── Meat dish restaurant.json
   │  │  │     │  │  ├── Momo restaurant.json
   │  │  │     │  │  ├── Musical club.json
   │  │  │     │  │  ├── Nepalese restaurant.json
   │  │  │     │  │  ├── Pizza restaurant.json
   │  │  │     │  │  ├── Pub.json
   │  │  │     │  │  ├── Restaurant or cafe.json
   │  │  │     │  │  ├── Restaurant.json
   │  │  │     │  │  ├── Rice restaurant.json
   │  │  │     │  │  ├── Sports bar.json
   │  │  │     │  │  ├── Tea house.json
   │  │  │     │  │  ├── Tea store.json
   │  │  │     │  │  ├── Thai restaurant.json
   │  │  │     │  │  ├── Vegetarian restaurant.json
   │  │  │     │  │  ├── Wholesale bakery.json
   │  │  │     │  │  └── Wine bar.json
   │  │  │     │  ├── cafe_apify.json
   │  │  │     │  ├── csv
   │  │  │     │  │  ├── compact_summary copy.csv
   │  │  │     │  │  ├── compact_summary.csv
   │  │  │     │  │  ├── compact_summary.geojson
   │  │  │     │  │  ├── compact_summary_generated.csv
   │  │  │     │  │  ├── compact_summary_images.csv
   │  │  │     │  │  ├── compact_summary_merged.csv
   │  │  │     │  │  ├── flattened_all_fields.csv
   │  │  │     │  │  └── generated_report.csv
   │  │  │     │  ├── flatfetch.py
   │  │  │     │  ├── flattened_places_numeric.csv
   │  │  │     │  ├── insideBhaktapur.json
   │  │  │     │  ├── otherParts.json
   │  │  │     │  ├── output
   │  │  │     │  ├── outsideBhaktapur.json
   │  │  │     │  ├── split_by_category.py
   │  │  │     │  └── venv
   │  │  │     │    ├── bin
   │  │  │     │     │  ├── activate
   │  │  │     │     │  ├── activate.csh
   │  │  │     │     │  ├── activate.fish
   │  │  │     │     │  ├── Activate.ps1
   │  │  │     │     │  ├── f2py
   │  │  │     │     │  ├── numpy-config
   │  │  │     │     │  ├── pip
   │  │  │     │     │  ├── pip3
   │  │  │     │     │  ├── pip3.13
   │  │  │     │     │  ├── python
   │  │  │     │     │  ├── python3
   │  │  │     │     │  └── python3.13
   │  │  │     │    ├── include
   │  │  │     │     │  └── python3.13
   │  │  │     │    ├── lib
   │  │  │     │     │  └── python3.13
   │  │  │     │     │    └── site-packages
   │  │  │     │     │       ├── dateutil
   │  │  │     │     │        │  ├── easter.py
   │  │  │     │     │        │  ├── parser
   │  │  │     │     │        │  │  ├── isoparser.py
   │  │  │     │     │        │  │  ├── _parser.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── relativedelta.py
   │  │  │     │     │        │  ├── rrule.py
   │  │  │     │     │        │  ├── tz
   │  │  │     │     │        │  │  ├── tz.py
   │  │  │     │     │        │  │  ├── win.py
   │  │  │     │     │        │  │  ├── _common.py
   │  │  │     │     │        │  │  ├── _factories.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── tzwin.py
   │  │  │     │     │        │  ├── utils.py
   │  │  │     │     │        │  ├── zoneinfo
   │  │  │     │     │        │  │  ├── dateutil-zoneinfo.tar.gz
   │  │  │     │     │        │  │  ├── rebuild.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── _common.py
   │  │  │     │     │        │  ├── _version.py
   │  │  │     │     │        │  └── __init__.py
   │  │  │     │     │       ├── numpy
   │  │  │     │     │        │  ├── char
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── conftest.py
   │  │  │     │     │        │  ├── core
   │  │  │     │     │        │  │  ├── arrayprint.py
   │  │  │     │     │        │  │  ├── defchararray.py
   │  │  │     │     │        │  │  ├── einsumfunc.py
   │  │  │     │     │        │  │  ├── fromnumeric.py
   │  │  │     │     │        │  │  ├── function_base.py
   │  │  │     │     │        │  │  ├── getlimits.py
   │  │  │     │     │        │  │  ├── multiarray.py
   │  │  │     │     │        │  │  ├── numeric.py
   │  │  │     │     │        │  │  ├── numerictypes.py
   │  │  │     │     │        │  │  ├── overrides.py
   │  │  │     │     │        │  │  ├── overrides.pyi
   │  │  │     │     │        │  │  ├── records.py
   │  │  │     │     │        │  │  ├── shape_base.py
   │  │  │     │     │        │  │  ├── umath.py
   │  │  │     │     │        │  │  ├── _dtype.py
   │  │  │     │     │        │  │  ├── _dtype.pyi
   │  │  │     │     │        │  │  ├── _dtype_ctypes.py
   │  │  │     │     │        │  │  ├── _dtype_ctypes.pyi
   │  │  │     │     │        │  │  ├── _internal.py
   │  │  │     │     │        │  │  ├── _multiarray_umath.py
   │  │  │     │     │        │  │  ├── _utils.py
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── ctypeslib
   │  │  │     │     │        │  │  ├── _ctypeslib.py
   │  │  │     │     │        │  │  ├── _ctypeslib.pyi
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── doc
   │  │  │     │     │        │  │  └── ufuncs.py
   │  │  │     │     │        │  ├── dtypes.py
   │  │  │     │     │        │  ├── dtypes.pyi
   │  │  │     │     │        │  ├── exceptions.py
   │  │  │     │     │        │  ├── exceptions.pyi
   │  │  │     │     │        │  ├── f2py
   │  │  │     │     │        │  │  ├── auxfuncs.py
   │  │  │     │     │        │  │  ├── auxfuncs.pyi
   │  │  │     │     │        │  │  ├── capi_maps.py
   │  │  │     │     │        │  │  ├── capi_maps.pyi
   │  │  │     │     │        │  │  ├── cb_rules.py
   │  │  │     │     │        │  │  ├── cb_rules.pyi
   │  │  │     │     │        │  │  ├── cfuncs.py
   │  │  │     │     │        │  │  ├── cfuncs.pyi
   │  │  │     │     │        │  │  ├── common_rules.py
   │  │  │     │     │        │  │  ├── common_rules.pyi
   │  │  │     │     │        │  │  ├── crackfortran.py
   │  │  │     │     │        │  │  ├── crackfortran.pyi
   │  │  │     │     │        │  │  ├── diagnose.py
   │  │  │     │     │        │  │  ├── diagnose.pyi
   │  │  │     │     │        │  │  ├── f2py2e.py
   │  │  │     │     │        │  │  ├── f2py2e.pyi
   │  │  │     │     │        │  │  ├── f90mod_rules.py
   │  │  │     │     │        │  │  ├── f90mod_rules.pyi
   │  │  │     │     │        │  │  ├── func2subr.py
   │  │  │     │     │        │  │  ├── func2subr.pyi
   │  │  │     │     │        │  │  ├── rules.py
   │  │  │     │     │        │  │  ├── rules.pyi
   │  │  │     │     │        │  │  ├── setup.cfg
   │  │  │     │     │        │  │  ├── src
   │  │  │     │     │        │  │  │  ├── fortranobject.c
   │  │  │     │     │        │  │  │  └── fortranobject.h
   │  │  │     │     │        │  │  ├── symbolic.py
   │  │  │     │     │        │  │  ├── symbolic.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── src
   │  │  │     │     │        │  │  │  │  ├── abstract_interface
   │  │  │     │     │        │  │  │  │  │  ├── foo.f90
   │  │  │     │     │        │  │  │  │  │  └── gh18403_mod.f90
   │  │  │     │     │        │  │  │  │  ├── array_from_pyobj
   │  │  │     │     │        │  │  │  │  │  └── wrapmodule.c
   │  │  │     │     │        │  │  │  │  ├── assumed_shape
   │  │  │     │     │        │  │  │  │  │  ├── foo_free.f90
   │  │  │     │     │        │  │  │  │  │  ├── foo_mod.f90
   │  │  │     │     │        │  │  │  │  │  ├── foo_use.f90
   │  │  │     │     │        │  │  │  │  │  └── precision.f90
   │  │  │     │     │        │  │  │  │  ├── block_docstring
   │  │  │     │     │        │  │  │  │  │  └── foo.f
   │  │  │     │     │        │  │  │  │  ├── callback
   │  │  │     │     │        │  │  │  │  │  ├── foo.f
   │  │  │     │     │        │  │  │  │  │  ├── gh17797.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh18335.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh25211.f
   │  │  │     │     │        │  │  │  │  │  ├── gh25211.pyf
   │  │  │     │     │        │  │  │  │  │  └── gh26681.f90
   │  │  │     │     │        │  │  │  │  ├── cli
   │  │  │     │     │        │  │  │  │  │  ├── gh_22819.pyf
   │  │  │     │     │        │  │  │  │  │  ├── hi77.f
   │  │  │     │     │        │  │  │  │  │  └── hiworld.f90
   │  │  │     │     │        │  │  │  │  ├── common
   │  │  │     │     │        │  │  │  │  │  ├── block.f
   │  │  │     │     │        │  │  │  │  │  └── gh19161.f90
   │  │  │     │     │        │  │  │  │  ├── crackfortran
   │  │  │     │     │        │  │  │  │  │  ├── accesstype.f90
   │  │  │     │     │        │  │  │  │  │  ├── common_with_division.f
   │  │  │     │     │        │  │  │  │  │  ├── data_common.f
   │  │  │     │     │        │  │  │  │  │  ├── data_multiplier.f
   │  │  │     │     │        │  │  │  │  │  ├── data_stmts.f90
   │  │  │     │     │        │  │  │  │  │  ├── data_with_comments.f
   │  │  │     │     │        │  │  │  │  │  ├── foo_deps.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh15035.f
   │  │  │     │     │        │  │  │  │  │  ├── gh17859.f
   │  │  │     │     │        │  │  │  │  │  ├── gh22648.pyf
   │  │  │     │     │        │  │  │  │  │  ├── gh23533.f
   │  │  │     │     │        │  │  │  │  │  ├── gh23598.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh23598Warn.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh23879.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh27697.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh2848.f90
   │  │  │     │     │        │  │  │  │  │  ├── operators.f90
   │  │  │     │     │        │  │  │  │  │  ├── privatemod.f90
   │  │  │     │     │        │  │  │  │  │  ├── publicmod.f90
   │  │  │     │     │        │  │  │  │  │  ├── pubprivmod.f90
   │  │  │     │     │        │  │  │  │  │  └── unicode_comment.f90
   │  │  │     │     │        │  │  │  │  ├── f2cmap
   │  │  │     │     │        │  │  │  │  │  └── isoFortranEnvMap.f90
   │  │  │     │     │        │  │  │  │  ├── isocintrin
   │  │  │     │     │        │  │  │  │  │  └── isoCtests.f90
   │  │  │     │     │        │  │  │  │  ├── kind
   │  │  │     │     │        │  │  │  │  │  └── foo.f90
   │  │  │     │     │        │  │  │  │  ├── mixed
   │  │  │     │     │        │  │  │  │  │  ├── foo.f
   │  │  │     │     │        │  │  │  │  │  ├── foo_fixed.f90
   │  │  │     │     │        │  │  │  │  │  └── foo_free.f90
   │  │  │     │     │        │  │  │  │  ├── modules
   │  │  │     │     │        │  │  │  │  │  ├── gh25337
   │  │  │     │     │        │  │  │  │  │  │  ├── data.f90
   │  │  │     │     │        │  │  │  │  │  │  └── use_data.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh26920
   │  │  │     │     │        │  │  │  │  │  │  ├── two_mods_with_no_public_entities.f90
   │  │  │     │     │        │  │  │  │  │  │  └── two_mods_with_one_public_routine.f90
   │  │  │     │     │        │  │  │  │  │  ├── module_data_docstring.f90
   │  │  │     │     │        │  │  │  │  │  └── use_modules.f90
   │  │  │     │     │        │  │  │  │  ├── negative_bounds
   │  │  │     │     │        │  │  │  │  │  └── issue_20853.f90
   │  │  │     │     │        │  │  │  │  ├── parameter
   │  │  │     │     │        │  │  │  │  │  ├── constant_array.f90
   │  │  │     │     │        │  │  │  │  │  ├── constant_both.f90
   │  │  │     │     │        │  │  │  │  │  ├── constant_compound.f90
   │  │  │     │     │        │  │  │  │  │  ├── constant_integer.f90
   │  │  │     │     │        │  │  │  │  │  ├── constant_non_compound.f90
   │  │  │     │     │        │  │  │  │  │  └── constant_real.f90
   │  │  │     │     │        │  │  │  │  ├── quoted_character
   │  │  │     │     │        │  │  │  │  │  └── foo.f
   │  │  │     │     │        │  │  │  │  ├── regression
   │  │  │     │     │        │  │  │  │  │  ├── AB.inc
   │  │  │     │     │        │  │  │  │  │  ├── assignOnlyModule.f90
   │  │  │     │     │        │  │  │  │  │  ├── datonly.f90
   │  │  │     │     │        │  │  │  │  │  ├── f77comments.f
   │  │  │     │     │        │  │  │  │  │  ├── f77fixedform.f95
   │  │  │     │     │        │  │  │  │  │  ├── f90continuation.f90
   │  │  │     │     │        │  │  │  │  │  ├── incfile.f90
   │  │  │     │     │        │  │  │  │  │  ├── inout.f90
   │  │  │     │     │        │  │  │  │  │  ├── lower_f2py_fortran.f90
   │  │  │     │     │        │  │  │  │  │  └── mod_derived_types.f90
   │  │  │     │     │        │  │  │  │  ├── return_character
   │  │  │     │     │        │  │  │  │  │  ├── foo77.f
   │  │  │     │     │        │  │  │  │  │  └── foo90.f90
   │  │  │     │     │        │  │  │  │  ├── return_complex
   │  │  │     │     │        │  │  │  │  │  ├── foo77.f
   │  │  │     │     │        │  │  │  │  │  └── foo90.f90
   │  │  │     │     │        │  │  │  │  ├── return_integer
   │  │  │     │     │        │  │  │  │  │  ├── foo77.f
   │  │  │     │     │        │  │  │  │  │  └── foo90.f90
   │  │  │     │     │        │  │  │  │  ├── return_logical
   │  │  │     │     │        │  │  │  │  │  ├── foo77.f
   │  │  │     │     │        │  │  │  │  │  └── foo90.f90
   │  │  │     │     │        │  │  │  │  ├── return_real
   │  │  │     │     │        │  │  │  │  │  ├── foo77.f
   │  │  │     │     │        │  │  │  │  │  └── foo90.f90
   │  │  │     │     │        │  │  │  │  ├── routines
   │  │  │     │     │        │  │  │  │  │  ├── funcfortranname.f
   │  │  │     │     │        │  │  │  │  │  ├── funcfortranname.pyf
   │  │  │     │     │        │  │  │  │  │  ├── subrout.f
   │  │  │     │     │        │  │  │  │  │  └── subrout.pyf
   │  │  │     │     │        │  │  │  │  ├── size
   │  │  │     │     │        │  │  │  │  │  └── foo.f90
   │  │  │     │     │        │  │  │  │  ├── string
   │  │  │     │     │        │  │  │  │  │  ├── char.f90
   │  │  │     │     │        │  │  │  │  │  ├── fixed_string.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh24008.f
   │  │  │     │     │        │  │  │  │  │  ├── gh24662.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh25286.f90
   │  │  │     │     │        │  │  │  │  │  ├── gh25286.pyf
   │  │  │     │     │        │  │  │  │  │  ├── gh25286_bc.pyf
   │  │  │     │     │        │  │  │  │  │  ├── scalar_string.f90
   │  │  │     │     │        │  │  │  │  │  └── string.f
   │  │  │     │     │        │  │  │  │  └── value_attrspec
   │  │  │     │     │        │  │  │  │    └── gh21665.f90
   │  │  │     │     │        │  │  │  ├── test_abstract_interface.py
   │  │  │     │     │        │  │  │  ├── test_array_from_pyobj.py
   │  │  │     │     │        │  │  │  ├── test_assumed_shape.py
   │  │  │     │     │        │  │  │  ├── test_block_docstring.py
   │  │  │     │     │        │  │  │  ├── test_callback.py
   │  │  │     │     │        │  │  │  ├── test_character.py
   │  │  │     │     │        │  │  │  ├── test_common.py
   │  │  │     │     │        │  │  │  ├── test_crackfortran.py
   │  │  │     │     │        │  │  │  ├── test_data.py
   │  │  │     │     │        │  │  │  ├── test_docs.py
   │  │  │     │     │        │  │  │  ├── test_f2cmap.py
   │  │  │     │     │        │  │  │  ├── test_f2py2e.py
   │  │  │     │     │        │  │  │  ├── test_isoc.py
   │  │  │     │     │        │  │  │  ├── test_kind.py
   │  │  │     │     │        │  │  │  ├── test_mixed.py
   │  │  │     │     │        │  │  │  ├── test_modules.py
   │  │  │     │     │        │  │  │  ├── test_parameter.py
   │  │  │     │     │        │  │  │  ├── test_pyf_src.py
   │  │  │     │     │        │  │  │  ├── test_quoted_character.py
   │  │  │     │     │        │  │  │  ├── test_regression.py
   │  │  │     │     │        │  │  │  ├── test_return_character.py
   │  │  │     │     │        │  │  │  ├── test_return_complex.py
   │  │  │     │     │        │  │  │  ├── test_return_integer.py
   │  │  │     │     │        │  │  │  ├── test_return_logical.py
   │  │  │     │     │        │  │  │  ├── test_return_real.py
   │  │  │     │     │        │  │  │  ├── test_routines.py
   │  │  │     │     │        │  │  │  ├── test_semicolon_split.py
   │  │  │     │     │        │  │  │  ├── test_size.py
   │  │  │     │     │        │  │  │  ├── test_string.py
   │  │  │     │     │        │  │  │  ├── test_symbolic.py
   │  │  │     │     │        │  │  │  ├── test_value_attrspec.py
   │  │  │     │     │        │  │  │  ├── util.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── use_rules.py
   │  │  │     │     │        │  │  ├── use_rules.pyi
   │  │  │     │     │        │  │  ├── _backends
   │  │  │     │     │        │  │  │  ├── meson.build.template
   │  │  │     │     │        │  │  │  ├── _backend.py
   │  │  │     │     │        │  │  │  ├── _backend.pyi
   │  │  │     │     │        │  │  │  ├── _distutils.py
   │  │  │     │     │        │  │  │  ├── _distutils.pyi
   │  │  │     │     │        │  │  │  ├── _meson.py
   │  │  │     │     │        │  │  │  ├── _meson.pyi
   │  │  │     │     │        │  │  │  ├── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.pyi
   │  │  │     │     │        │  │  ├── _isocbind.py
   │  │  │     │     │        │  │  ├── _isocbind.pyi
   │  │  │     │     │        │  │  ├── _src_pyf.py
   │  │  │     │     │        │  │  ├── _src_pyf.pyi
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  ├── __init__.pyi
   │  │  │     │     │        │  │  ├── __main__.py
   │  │  │     │     │        │  │  ├── __version__.py
   │  │  │     │     │        │  │  └── __version__.pyi
   │  │  │     │     │        │  ├── fft
   │  │  │     │     │        │  │  ├── helper.py
   │  │  │     │     │        │  │  ├── helper.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── test_helper.py
   │  │  │     │     │        │  │  │  ├── test_pocketfft.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── _helper.py
   │  │  │     │     │        │  │  ├── _helper.pyi
   │  │  │     │     │        │  │  ├── _pocketfft.py
   │  │  │     │     │        │  │  ├── _pocketfft.pyi
   │  │  │     │     │        │  │  ├── _pocketfft_umath.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── lib
   │  │  │     │     │        │  │  ├── array_utils.py
   │  │  │     │     │        │  │  ├── array_utils.pyi
   │  │  │     │     │        │  │  ├── format.py
   │  │  │     │     │        │  │  ├── format.pyi
   │  │  │     │     │        │  │  ├── introspect.py
   │  │  │     │     │        │  │  ├── introspect.pyi
   │  │  │     │     │        │  │  ├── mixins.py
   │  │  │     │     │        │  │  ├── mixins.pyi
   │  │  │     │     │        │  │  ├── npyio.py
   │  │  │     │     │        │  │  ├── npyio.pyi
   │  │  │     │     │        │  │  ├── recfunctions.py
   │  │  │     │     │        │  │  ├── recfunctions.pyi
   │  │  │     │     │        │  │  ├── scimath.py
   │  │  │     │     │        │  │  ├── scimath.pyi
   │  │  │     │     │        │  │  ├── stride_tricks.py
   │  │  │     │     │        │  │  ├── stride_tricks.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── data
   │  │  │     │     │        │  │  │  │  ├── py2-np0-objarr.npy
   │  │  │     │     │        │  │  │  │  ├── py2-objarr.npy
   │  │  │     │     │        │  │  │  │  ├── py2-objarr.npz
   │  │  │     │     │        │  │  │  │  ├── py3-objarr.npy
   │  │  │     │     │        │  │  │  │  ├── py3-objarr.npz
   │  │  │     │     │        │  │  │  │  ├── python3.npy
   │  │  │     │     │        │  │  │  │  └── win64python2.npy
   │  │  │     │     │        │  │  │  ├── test_arraypad.py
   │  │  │     │     │        │  │  │  ├── test_arraysetops.py
   │  │  │     │     │        │  │  │  ├── test_arrayterator.py
   │  │  │     │     │        │  │  │  ├── test_array_utils.py
   │  │  │     │     │        │  │  │  ├── test_format.py
   │  │  │     │     │        │  │  │  ├── test_function_base.py
   │  │  │     │     │        │  │  │  ├── test_histograms.py
   │  │  │     │     │        │  │  │  ├── test_index_tricks.py
   │  │  │     │     │        │  │  │  ├── test_io.py
   │  │  │     │     │        │  │  │  ├── test_loadtxt.py
   │  │  │     │     │        │  │  │  ├── test_mixins.py
   │  │  │     │     │        │  │  │  ├── test_nanfunctions.py
   │  │  │     │     │        │  │  │  ├── test_packbits.py
   │  │  │     │     │        │  │  │  ├── test_polynomial.py
   │  │  │     │     │        │  │  │  ├── test_recfunctions.py
   │  │  │     │     │        │  │  │  ├── test_regression.py
   │  │  │     │     │        │  │  │  ├── test_shape_base.py
   │  │  │     │     │        │  │  │  ├── test_stride_tricks.py
   │  │  │     │     │        │  │  │  ├── test_twodim_base.py
   │  │  │     │     │        │  │  │  ├── test_type_check.py
   │  │  │     │     │        │  │  │  ├── test_ufunclike.py
   │  │  │     │     │        │  │  │  ├── test_utils.py
   │  │  │     │     │        │  │  │  ├── test__datasource.py
   │  │  │     │     │        │  │  │  ├── test__iotools.py
   │  │  │     │     │        │  │  │  ├── test__version.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── user_array.py
   │  │  │     │     │        │  │  ├── user_array.pyi
   │  │  │     │     │        │  │  ├── _arraypad_impl.py
   │  │  │     │     │        │  │  ├── _arraypad_impl.pyi
   │  │  │     │     │        │  │  ├── _arraysetops_impl.py
   │  │  │     │     │        │  │  ├── _arraysetops_impl.pyi
   │  │  │     │     │        │  │  ├── _arrayterator_impl.py
   │  │  │     │     │        │  │  ├── _arrayterator_impl.pyi
   │  │  │     │     │        │  │  ├── _array_utils_impl.py
   │  │  │     │     │        │  │  ├── _array_utils_impl.pyi
   │  │  │     │     │        │  │  ├── _datasource.py
   │  │  │     │     │        │  │  ├── _datasource.pyi
   │  │  │     │     │        │  │  ├── _format_impl.py
   │  │  │     │     │        │  │  ├── _format_impl.pyi
   │  │  │     │     │        │  │  ├── _function_base_impl.py
   │  │  │     │     │        │  │  ├── _function_base_impl.pyi
   │  │  │     │     │        │  │  ├── _histograms_impl.py
   │  │  │     │     │        │  │  ├── _histograms_impl.pyi
   │  │  │     │     │        │  │  ├── _index_tricks_impl.py
   │  │  │     │     │        │  │  ├── _index_tricks_impl.pyi
   │  │  │     │     │        │  │  ├── _iotools.py
   │  │  │     │     │        │  │  ├── _iotools.pyi
   │  │  │     │     │        │  │  ├── _nanfunctions_impl.py
   │  │  │     │     │        │  │  ├── _nanfunctions_impl.pyi
   │  │  │     │     │        │  │  ├── _npyio_impl.py
   │  │  │     │     │        │  │  ├── _npyio_impl.pyi
   │  │  │     │     │        │  │  ├── _polynomial_impl.py
   │  │  │     │     │        │  │  ├── _polynomial_impl.pyi
   │  │  │     │     │        │  │  ├── _scimath_impl.py
   │  │  │     │     │        │  │  ├── _scimath_impl.pyi
   │  │  │     │     │        │  │  ├── _shape_base_impl.py
   │  │  │     │     │        │  │  ├── _shape_base_impl.pyi
   │  │  │     │     │        │  │  ├── _stride_tricks_impl.py
   │  │  │     │     │        │  │  ├── _stride_tricks_impl.pyi
   │  │  │     │     │        │  │  ├── _twodim_base_impl.py
   │  │  │     │     │        │  │  ├── _twodim_base_impl.pyi
   │  │  │     │     │        │  │  ├── _type_check_impl.py
   │  │  │     │     │        │  │  ├── _type_check_impl.pyi
   │  │  │     │     │        │  │  ├── _ufunclike_impl.py
   │  │  │     │     │        │  │  ├── _ufunclike_impl.pyi
   │  │  │     │     │        │  │  ├── _user_array_impl.py
   │  │  │     │     │        │  │  ├── _user_array_impl.pyi
   │  │  │     │     │        │  │  ├── _utils_impl.py
   │  │  │     │     │        │  │  ├── _utils_impl.pyi
   │  │  │     │     │        │  │  ├── _version.py
   │  │  │     │     │        │  │  ├── _version.pyi
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── linalg
   │  │  │     │     │        │  │  ├── lapack_lite.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── lapack_lite.pyi
   │  │  │     │     │        │  │  ├── linalg.py
   │  │  │     │     │        │  │  ├── linalg.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── test_deprecations.py
   │  │  │     │     │        │  │  │  ├── test_linalg.py
   │  │  │     │     │        │  │  │  ├── test_regression.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── _linalg.py
   │  │  │     │     │        │  │  ├── _linalg.pyi
   │  │  │     │     │        │  │  ├── _umath_linalg.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _umath_linalg.pyi
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── ma
   │  │  │     │     │        │  │  ├── API_CHANGES.txt
   │  │  │     │     │        │  │  ├── core.py
   │  │  │     │     │        │  │  ├── core.pyi
   │  │  │     │     │        │  │  ├── extras.py
   │  │  │     │     │        │  │  ├── extras.pyi
   │  │  │     │     │        │  │  ├── LICENSE
   │  │  │     │     │        │  │  ├── mrecords.py
   │  │  │     │     │        │  │  ├── mrecords.pyi
   │  │  │     │     │        │  │  ├── README.rst
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── test_arrayobject.py
   │  │  │     │     │        │  │  │  ├── test_core.py
   │  │  │     │     │        │  │  │  ├── test_deprecations.py
   │  │  │     │     │        │  │  │  ├── test_extras.py
   │  │  │     │     │        │  │  │  ├── test_mrecords.py
   │  │  │     │     │        │  │  │  ├── test_old_ma.py
   │  │  │     │     │        │  │  │  ├── test_regression.py
   │  │  │     │     │        │  │  │  ├── test_subclassing.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── testutils.py
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── matlib.py
   │  │  │     │     │        │  ├── matlib.pyi
   │  │  │     │     │        │  ├── matrixlib
   │  │  │     │     │        │  │  ├── defmatrix.py
   │  │  │     │     │        │  │  ├── defmatrix.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── test_defmatrix.py
   │  │  │     │     │        │  │  │  ├── test_interaction.py
   │  │  │     │     │        │  │  │  ├── test_masked_matrix.py
   │  │  │     │     │        │  │  │  ├── test_matrix_linalg.py
   │  │  │     │     │        │  │  │  ├── test_multiarray.py
   │  │  │     │     │        │  │  │  ├── test_numeric.py
   │  │  │     │     │        │  │  │  ├── test_regression.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── polynomial
   │  │  │     │     │        │  │  ├── chebyshev.py
   │  │  │     │     │        │  │  ├── chebyshev.pyi
   │  │  │     │     │        │  │  ├── hermite.py
   │  │  │     │     │        │  │  ├── hermite.pyi
   │  │  │     │     │        │  │  ├── hermite_e.py
   │  │  │     │     │        │  │  ├── hermite_e.pyi
   │  │  │     │     │        │  │  ├── laguerre.py
   │  │  │     │     │        │  │  ├── laguerre.pyi
   │  │  │     │     │        │  │  ├── legendre.py
   │  │  │     │     │        │  │  ├── legendre.pyi
   │  │  │     │     │        │  │  ├── polynomial.py
   │  │  │     │     │        │  │  ├── polynomial.pyi
   │  │  │     │     │        │  │  ├── polyutils.py
   │  │  │     │     │        │  │  ├── polyutils.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── test_chebyshev.py
   │  │  │     │     │        │  │  │  ├── test_classes.py
   │  │  │     │     │        │  │  │  ├── test_hermite.py
   │  │  │     │     │        │  │  │  ├── test_hermite_e.py
   │  │  │     │     │        │  │  │  ├── test_laguerre.py
   │  │  │     │     │        │  │  │  ├── test_legendre.py
   │  │  │     │     │        │  │  │  ├── test_polynomial.py
   │  │  │     │     │        │  │  │  ├── test_polyutils.py
   │  │  │     │     │        │  │  │  ├── test_printing.py
   │  │  │     │     │        │  │  │  ├── test_symbol.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── _polybase.py
   │  │  │     │     │        │  │  ├── _polybase.pyi
   │  │  │     │     │        │  │  ├── _polytypes.pyi
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── py.typed
   │  │  │     │     │        │  ├── random
   │  │  │     │     │        │  │  ├── bit_generator.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── bit_generator.pxd
   │  │  │     │     │        │  │  ├── bit_generator.pyi
   │  │  │     │     │        │  │  ├── c_distributions.pxd
   │  │  │     │     │        │  │  ├── lib
   │  │  │     │     │        │  │  │  └── libnpyrandom.a
   │  │  │     │     │        │  │  ├── LICENSE.md
   │  │  │     │     │        │  │  ├── mtrand.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── mtrand.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── data
   │  │  │     │     │        │  │  │  │  ├── generator_pcg64_np121.pkl.gz
   │  │  │     │     │        │  │  │  │  ├── generator_pcg64_np126.pkl.gz
   │  │  │     │     │        │  │  │  │  ├── mt19937-testset-1.csv
   │  │  │     │     │        │  │  │  │  ├── mt19937-testset-2.csv
   │  │  │     │     │        │  │  │  │  ├── pcg64-testset-1.csv
   │  │  │     │     │        │  │  │  │  ├── pcg64-testset-2.csv
   │  │  │     │     │        │  │  │  │  ├── pcg64dxsm-testset-1.csv
   │  │  │     │     │        │  │  │  │  ├── pcg64dxsm-testset-2.csv
   │  │  │     │     │        │  │  │  │  ├── philox-testset-1.csv
   │  │  │     │     │        │  │  │  │  ├── philox-testset-2.csv
   │  │  │     │     │        │  │  │  │  ├── sfc64-testset-1.csv
   │  │  │     │     │        │  │  │  │  ├── sfc64-testset-2.csv
   │  │  │     │     │        │  │  │  │  ├── sfc64_np126.pkl.gz
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_direct.py
   │  │  │     │     │        │  │  │  ├── test_extending.py
   │  │  │     │     │        │  │  │  ├── test_generator_mt19937.py
   │  │  │     │     │        │  │  │  ├── test_generator_mt19937_regressions.py
   │  │  │     │     │        │  │  │  ├── test_random.py
   │  │  │     │     │        │  │  │  ├── test_randomstate.py
   │  │  │     │     │        │  │  │  ├── test_randomstate_regression.py
   │  │  │     │     │        │  │  │  ├── test_regression.py
   │  │  │     │     │        │  │  │  ├── test_seed_sequence.py
   │  │  │     │     │        │  │  │  ├── test_smoke.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── _bounded_integers.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _bounded_integers.pxd
   │  │  │     │     │        │  │  ├── _bounded_integers.pyi
   │  │  │     │     │        │  │  ├── _common.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _common.pxd
   │  │  │     │     │        │  │  ├── _common.pyi
   │  │  │     │     │        │  │  ├── _examples
   │  │  │     │     │        │  │  │  ├── cffi
   │  │  │     │     │        │  │  │  │  ├── extending.py
   │  │  │     │     │        │  │  │  │  └── parse.py
   │  │  │     │     │        │  │  │  ├── cython
   │  │  │     │     │        │  │  │  │  ├── extending.pyx
   │  │  │     │     │        │  │  │  │  ├── extending_distributions.pyx
   │  │  │     │     │        │  │  │  │  └── meson.build
   │  │  │     │     │        │  │  │  └── numba
   │  │  │     │     │        │  │  │    ├── extending.py
   │  │  │     │     │        │  │  │    └── extending_distributions.py
   │  │  │     │     │        │  │  ├── _generator.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _generator.pyi
   │  │  │     │     │        │  │  ├── _mt19937.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _mt19937.pyi
   │  │  │     │     │        │  │  ├── _pcg64.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _pcg64.pyi
   │  │  │     │     │        │  │  ├── _philox.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _philox.pyi
   │  │  │     │     │        │  │  ├── _pickle.py
   │  │  │     │     │        │  │  ├── _pickle.pyi
   │  │  │     │     │        │  │  ├── _sfc64.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _sfc64.pyi
   │  │  │     │     │        │  │  ├── __init__.pxd
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── rec
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── strings
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── testing
   │  │  │     │     │        │  │  ├── overrides.py
   │  │  │     │     │        │  │  ├── overrides.pyi
   │  │  │     │     │        │  │  ├── print_coercion_tables.py
   │  │  │     │     │        │  │  ├── print_coercion_tables.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── test_utils.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── _private
   │  │  │     │     │        │  │  │  ├── extbuild.py
   │  │  │     │     │        │  │  │  ├── extbuild.pyi
   │  │  │     │     │        │  │  │  ├── utils.py
   │  │  │     │     │        │  │  │  ├── utils.pyi
   │  │  │     │     │        │  │  │  ├── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.pyi
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── tests
   │  │  │     │     │        │  │  ├── test_configtool.py
   │  │  │     │     │        │  │  ├── test_ctypeslib.py
   │  │  │     │     │        │  │  ├── test_lazyloading.py
   │  │  │     │     │        │  │  ├── test_matlib.py
   │  │  │     │     │        │  │  ├── test_numpy_config.py
   │  │  │     │     │        │  │  ├── test_numpy_version.py
   │  │  │     │     │        │  │  ├── test_public_api.py
   │  │  │     │     │        │  │  ├── test_reloading.py
   │  │  │     │     │        │  │  ├── test_scripts.py
   │  │  │     │     │        │  │  ├── test_warnings.py
   │  │  │     │     │        │  │  ├── test__all__.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── typing
   │  │  │     │     │        │  │  ├── mypy_plugin.py
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── data
   │  │  │     │     │        │  │  │  │  ├── fail
   │  │  │     │     │        │  │  │  │  │  ├── arithmetic.pyi
   │  │  │     │     │        │  │  │  │  │  ├── arrayprint.pyi
   │  │  │     │     │        │  │  │  │  │  ├── arrayterator.pyi
   │  │  │     │     │        │  │  │  │  │  ├── array_constructors.pyi
   │  │  │     │     │        │  │  │  │  │  ├── array_like.pyi
   │  │  │     │     │        │  │  │  │  │  ├── array_pad.pyi
   │  │  │     │     │        │  │  │  │  │  ├── bitwise_ops.pyi
   │  │  │     │     │        │  │  │  │  │  ├── char.pyi
   │  │  │     │     │        │  │  │  │  │  ├── chararray.pyi
   │  │  │     │     │        │  │  │  │  │  ├── comparisons.pyi
   │  │  │     │     │        │  │  │  │  │  ├── constants.pyi
   │  │  │     │     │        │  │  │  │  │  ├── datasource.pyi
   │  │  │     │     │        │  │  │  │  │  ├── dtype.pyi
   │  │  │     │     │        │  │  │  │  │  ├── einsumfunc.pyi
   │  │  │     │     │        │  │  │  │  │  ├── flatiter.pyi
   │  │  │     │     │        │  │  │  │  │  ├── fromnumeric.pyi
   │  │  │     │     │        │  │  │  │  │  ├── histograms.pyi
   │  │  │     │     │        │  │  │  │  │  ├── index_tricks.pyi
   │  │  │     │     │        │  │  │  │  │  ├── lib_function_base.pyi
   │  │  │     │     │        │  │  │  │  │  ├── lib_polynomial.pyi
   │  │  │     │     │        │  │  │  │  │  ├── lib_utils.pyi
   │  │  │     │     │        │  │  │  │  │  ├── lib_version.pyi
   │  │  │     │     │        │  │  │  │  │  ├── linalg.pyi
   │  │  │     │     │        │  │  │  │  │  ├── ma.pyi
   │  │  │     │     │        │  │  │  │  │  ├── memmap.pyi
   │  │  │     │     │        │  │  │  │  │  ├── modules.pyi
   │  │  │     │     │        │  │  │  │  │  ├── multiarray.pyi
   │  │  │     │     │        │  │  │  │  │  ├── ndarray.pyi
   │  │  │     │     │        │  │  │  │  │  ├── ndarray_misc.pyi
   │  │  │     │     │        │  │  │  │  │  ├── nditer.pyi
   │  │  │     │     │        │  │  │  │  │  ├── nested_sequence.pyi
   │  │  │     │     │        │  │  │  │  │  ├── npyio.pyi
   │  │  │     │     │        │  │  │  │  │  ├── numerictypes.pyi
   │  │  │     │     │        │  │  │  │  │  ├── random.pyi
   │  │  │     │     │        │  │  │  │  │  ├── rec.pyi
   │  │  │     │     │        │  │  │  │  │  ├── scalars.pyi
   │  │  │     │     │        │  │  │  │  │  ├── shape.pyi
   │  │  │     │     │        │  │  │  │  │  ├── shape_base.pyi
   │  │  │     │     │        │  │  │  │  │  ├── stride_tricks.pyi
   │  │  │     │     │        │  │  │  │  │  ├── strings.pyi
   │  │  │     │     │        │  │  │  │  │  ├── testing.pyi
   │  │  │     │     │        │  │  │  │  │  ├── twodim_base.pyi
   │  │  │     │     │        │  │  │  │  │  ├── type_check.pyi
   │  │  │     │     │        │  │  │  │  │  ├── ufunclike.pyi
   │  │  │     │     │        │  │  │  │  │  ├── ufuncs.pyi
   │  │  │     │     │        │  │  │  │  │  ├── ufunc_config.pyi
   │  │  │     │     │        │  │  │  │  │  └── warnings_and_errors.pyi
   │  │  │     │     │        │  │  │  │  ├── misc
   │  │  │     │     │        │  │  │  │  │  └── extended_precision.pyi
   │  │  │     │     │        │  │  │  │  ├── mypy.ini
   │  │  │     │     │        │  │  │  │  ├── pass
   │  │  │     │     │        │  │  │  │  │  ├── arithmetic.py
   │  │  │     │     │        │  │  │  │  │  ├── arrayprint.py
   │  │  │     │     │        │  │  │  │  │  ├── arrayterator.py
   │  │  │     │     │        │  │  │  │  │  ├── array_constructors.py
   │  │  │     │     │        │  │  │  │  │  ├── array_like.py
   │  │  │     │     │        │  │  │  │  │  ├── bitwise_ops.py
   │  │  │     │     │        │  │  │  │  │  ├── comparisons.py
   │  │  │     │     │        │  │  │  │  │  ├── dtype.py
   │  │  │     │     │        │  │  │  │  │  ├── einsumfunc.py
   │  │  │     │     │        │  │  │  │  │  ├── flatiter.py
   │  │  │     │     │        │  │  │  │  │  ├── fromnumeric.py
   │  │  │     │     │        │  │  │  │  │  ├── index_tricks.py
   │  │  │     │     │        │  │  │  │  │  ├── lib_user_array.py
   │  │  │     │     │        │  │  │  │  │  ├── lib_utils.py
   │  │  │     │     │        │  │  │  │  │  ├── lib_version.py
   │  │  │     │     │        │  │  │  │  │  ├── literal.py
   │  │  │     │     │        │  │  │  │  │  ├── ma.py
   │  │  │     │     │        │  │  │  │  │  ├── mod.py
   │  │  │     │     │        │  │  │  │  │  ├── modules.py
   │  │  │     │     │        │  │  │  │  │  ├── multiarray.py
   │  │  │     │     │        │  │  │  │  │  ├── ndarray_conversion.py
   │  │  │     │     │        │  │  │  │  │  ├── ndarray_misc.py
   │  │  │     │     │        │  │  │  │  │  ├── ndarray_shape_manipulation.py
   │  │  │     │     │        │  │  │  │  │  ├── nditer.py
   │  │  │     │     │        │  │  │  │  │  ├── numeric.py
   │  │  │     │     │        │  │  │  │  │  ├── numerictypes.py
   │  │  │     │     │        │  │  │  │  │  ├── random.py
   │  │  │     │     │        │  │  │  │  │  ├── recfunctions.py
   │  │  │     │     │        │  │  │  │  │  ├── scalars.py
   │  │  │     │     │        │  │  │  │  │  ├── shape.py
   │  │  │     │     │        │  │  │  │  │  ├── simple.py
   │  │  │     │     │        │  │  │  │  │  ├── simple_py3.py
   │  │  │     │     │        │  │  │  │  │  ├── ufunclike.py
   │  │  │     │     │        │  │  │  │  │  ├── ufuncs.py
   │  │  │     │     │        │  │  │  │  │  ├── ufunc_config.py
   │  │  │     │     │        │  │  │  │  │  └── warnings_and_errors.py
   │  │  │     │     │        │  │  │  │  └── reveal
   │  │  │     │     │        │  │  │  │    ├── arithmetic.pyi
   │  │  │     │     │        │  │  │  │    ├── arraypad.pyi
   │  │  │     │     │        │  │  │  │    ├── arrayprint.pyi
   │  │  │     │     │        │  │  │  │    ├── arraysetops.pyi
   │  │  │     │     │        │  │  │  │    ├── arrayterator.pyi
   │  │  │     │     │        │  │  │  │    ├── array_api_info.pyi
   │  │  │     │     │        │  │  │  │    ├── array_constructors.pyi
   │  │  │     │     │        │  │  │  │    ├── bitwise_ops.pyi
   │  │  │     │     │        │  │  │  │    ├── char.pyi
   │  │  │     │     │        │  │  │  │    ├── chararray.pyi
   │  │  │     │     │        │  │  │  │    ├── comparisons.pyi
   │  │  │     │     │        │  │  │  │    ├── constants.pyi
   │  │  │     │     │        │  │  │  │    ├── ctypeslib.pyi
   │  │  │     │     │        │  │  │  │    ├── datasource.pyi
   │  │  │     │     │        │  │  │  │    ├── dtype.pyi
   │  │  │     │     │        │  │  │  │    ├── einsumfunc.pyi
   │  │  │     │     │        │  │  │  │    ├── emath.pyi
   │  │  │     │     │        │  │  │  │    ├── fft.pyi
   │  │  │     │     │        │  │  │  │    ├── flatiter.pyi
   │  │  │     │     │        │  │  │  │    ├── fromnumeric.pyi
   │  │  │     │     │        │  │  │  │    ├── getlimits.pyi
   │  │  │     │     │        │  │  │  │    ├── histograms.pyi
   │  │  │     │     │        │  │  │  │    ├── index_tricks.pyi
   │  │  │     │     │        │  │  │  │    ├── lib_function_base.pyi
   │  │  │     │     │        │  │  │  │    ├── lib_polynomial.pyi
   │  │  │     │     │        │  │  │  │    ├── lib_utils.pyi
   │  │  │     │     │        │  │  │  │    ├── lib_version.pyi
   │  │  │     │     │        │  │  │  │    ├── linalg.pyi
   │  │  │     │     │        │  │  │  │    ├── ma.pyi
   │  │  │     │     │        │  │  │  │    ├── matrix.pyi
   │  │  │     │     │        │  │  │  │    ├── memmap.pyi
   │  │  │     │     │        │  │  │  │    ├── mod.pyi
   │  │  │     │     │        │  │  │  │    ├── modules.pyi
   │  │  │     │     │        │  │  │  │    ├── multiarray.pyi
   │  │  │     │     │        │  │  │  │    ├── nbit_base_example.pyi
   │  │  │     │     │        │  │  │  │    ├── ndarray_assignability.pyi
   │  │  │     │     │        │  │  │  │    ├── ndarray_conversion.pyi
   │  │  │     │     │        │  │  │  │    ├── ndarray_misc.pyi
   │  │  │     │     │        │  │  │  │    ├── ndarray_shape_manipulation.pyi
   │  │  │     │     │        │  │  │  │    ├── nditer.pyi
   │  │  │     │     │        │  │  │  │    ├── nested_sequence.pyi
   │  │  │     │     │        │  │  │  │    ├── npyio.pyi
   │  │  │     │     │        │  │  │  │    ├── numeric.pyi
   │  │  │     │     │        │  │  │  │    ├── numerictypes.pyi
   │  │  │     │     │        │  │  │  │    ├── polynomial_polybase.pyi
   │  │  │     │     │        │  │  │  │    ├── polynomial_polyutils.pyi
   │  │  │     │     │        │  │  │  │    ├── polynomial_series.pyi
   │  │  │     │     │        │  │  │  │    ├── random.pyi
   │  │  │     │     │        │  │  │  │    ├── rec.pyi
   │  │  │     │     │        │  │  │  │    ├── scalars.pyi
   │  │  │     │     │        │  │  │  │    ├── shape.pyi
   │  │  │     │     │        │  │  │  │    ├── shape_base.pyi
   │  │  │     │     │        │  │  │  │    ├── stride_tricks.pyi
   │  │  │     │     │        │  │  │  │    ├── strings.pyi
   │  │  │     │     │        │  │  │  │    ├── testing.pyi
   │  │  │     │     │        │  │  │  │    ├── twodim_base.pyi
   │  │  │     │     │        │  │  │  │    ├── type_check.pyi
   │  │  │     │     │        │  │  │  │    ├── ufunclike.pyi
   │  │  │     │     │        │  │  │  │    ├── ufuncs.pyi
   │  │  │     │     │        │  │  │  │    ├── ufunc_config.pyi
   │  │  │     │     │        │  │  │  │    └── warnings_and_errors.pyi
   │  │  │     │     │        │  │  │  ├── test_isfile.py
   │  │  │     │     │        │  │  │  ├── test_runtime.py
   │  │  │     │     │        │  │  │  ├── test_typing.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── version.py
   │  │  │     │     │        │  ├── version.pyi
   │  │  │     │     │        │  ├── _array_api_info.py
   │  │  │     │     │        │  ├── _array_api_info.pyi
   │  │  │     │     │        │  ├── _configtool.py
   │  │  │     │     │        │  ├── _configtool.pyi
   │  │  │     │     │        │  ├── _core
   │  │  │     │     │        │  │  ├── arrayprint.py
   │  │  │     │     │        │  │  ├── arrayprint.pyi
   │  │  │     │     │        │  │  ├── cversions.py
   │  │  │     │     │        │  │  ├── defchararray.py
   │  │  │     │     │        │  │  ├── defchararray.pyi
   │  │  │     │     │        │  │  ├── einsumfunc.py
   │  │  │     │     │        │  │  ├── einsumfunc.pyi
   │  │  │     │     │        │  │  ├── fromnumeric.py
   │  │  │     │     │        │  │  ├── fromnumeric.pyi
   │  │  │     │     │        │  │  ├── function_base.py
   │  │  │     │     │        │  │  ├── function_base.pyi
   │  │  │     │     │        │  │  ├── getlimits.py
   │  │  │     │     │        │  │  ├── getlimits.pyi
   │  │  │     │     │        │  │  ├── include
   │  │  │     │     │        │  │  │  └── numpy
   │  │  │     │     │        │  │  │    ├── arrayobject.h
   │  │  │     │     │        │  │  │    ├── arrayscalars.h
   │  │  │     │     │        │  │  │    ├── dtype_api.h
   │  │  │     │     │        │  │  │    ├── halffloat.h
   │  │  │     │     │        │  │  │    ├── ndarrayobject.h
   │  │  │     │     │        │  │  │    ├── ndarraytypes.h
   │  │  │     │     │        │  │  │    ├── npy_2_compat.h
   │  │  │     │     │        │  │  │    ├── npy_2_complexcompat.h
   │  │  │     │     │        │  │  │    ├── npy_3kcompat.h
   │  │  │     │     │        │  │  │    ├── npy_common.h
   │  │  │     │     │        │  │  │    ├── npy_cpu.h
   │  │  │     │     │        │  │  │    ├── npy_endian.h
   │  │  │     │     │        │  │  │    ├── npy_math.h
   │  │  │     │     │        │  │  │    ├── npy_no_deprecated_api.h
   │  │  │     │     │        │  │  │    ├── npy_os.h
   │  │  │     │     │        │  │  │    ├── numpyconfig.h
   │  │  │     │     │        │  │  │    ├── random
   │  │  │     │     │        │  │  │     │  ├── bitgen.h
   │  │  │     │     │        │  │  │     │  ├── distributions.h
   │  │  │     │     │        │  │  │     │  ├── libdivide.h
   │  │  │     │     │        │  │  │     │  └── LICENSE.txt
   │  │  │     │     │        │  │  │    ├── ufuncobject.h
   │  │  │     │     │        │  │  │    ├── utils.h
   │  │  │     │     │        │  │  │    ├── _neighborhood_iterator_imp.h
   │  │  │     │     │        │  │  │    ├── _numpyconfig.h
   │  │  │     │     │        │  │  │    ├── _public_dtype_api_table.h
   │  │  │     │     │        │  │  │    ├── __multiarray_api.c
   │  │  │     │     │        │  │  │    ├── __multiarray_api.h
   │  │  │     │     │        │  │  │    ├── __ufunc_api.c
   │  │  │     │     │        │  │  │    └── __ufunc_api.h
   │  │  │     │     │        │  │  ├── lib
   │  │  │     │     │        │  │  │  ├── libnpymath.a
   │  │  │     │     │        │  │  │  ├── npy-pkg-config
   │  │  │     │     │        │  │  │  │  ├── mlib.ini
   │  │  │     │     │        │  │  │  │  └── npymath.ini
   │  │  │     │     │        │  │  │  └── pkgconfig
   │  │  │     │     │        │  │  │    └── numpy.pc
   │  │  │     │     │        │  │  ├── memmap.py
   │  │  │     │     │        │  │  ├── memmap.pyi
   │  │  │     │     │        │  │  ├── multiarray.py
   │  │  │     │     │        │  │  ├── multiarray.pyi
   │  │  │     │     │        │  │  ├── numeric.py
   │  │  │     │     │        │  │  ├── numeric.pyi
   │  │  │     │     │        │  │  ├── numerictypes.py
   │  │  │     │     │        │  │  ├── numerictypes.pyi
   │  │  │     │     │        │  │  ├── overrides.py
   │  │  │     │     │        │  │  ├── overrides.pyi
   │  │  │     │     │        │  │  ├── printoptions.py
   │  │  │     │     │        │  │  ├── printoptions.pyi
   │  │  │     │     │        │  │  ├── records.py
   │  │  │     │     │        │  │  ├── records.pyi
   │  │  │     │     │        │  │  ├── shape_base.py
   │  │  │     │     │        │  │  ├── shape_base.pyi
   │  │  │     │     │        │  │  ├── strings.py
   │  │  │     │     │        │  │  ├── strings.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── data
   │  │  │     │     │        │  │  │  │  ├── astype_copy.pkl
   │  │  │     │     │        │  │  │  │  ├── generate_umath_validation_data.cpp
   │  │  │     │     │        │  │  │  │  ├── recarray_from_file.fits
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-arccos.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-arccosh.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-arcsin.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-arcsinh.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-arctan.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-arctanh.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-cbrt.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-cos.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-cosh.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-exp.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-exp2.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-expm1.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-log.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-log10.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-log1p.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-log2.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-README.txt
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-sin.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-sinh.csv
   │  │  │     │     │        │  │  │  │  ├── umath-validation-set-tan.csv
   │  │  │     │     │        │  │  │  │  └── umath-validation-set-tanh.csv
   │  │  │     │     │        │  │  │  ├── examples
   │  │  │     │     │        │  │  │  │  ├── cython
   │  │  │     │     │        │  │  │  │  │  ├── checks.pyx
   │  │  │     │     │        │  │  │  │  │  ├── meson.build
   │  │  │     │     │        │  │  │  │  │  └── setup.py
   │  │  │     │     │        │  │  │  │  └── limited_api
   │  │  │     │     │        │  │  │  │    ├── limited_api1.c
   │  │  │     │     │        │  │  │  │    ├── limited_api2.pyx
   │  │  │     │     │        │  │  │  │    ├── limited_api_latest.c
   │  │  │     │     │        │  │  │  │    ├── meson.build
   │  │  │     │     │        │  │  │  │    └── setup.py
   │  │  │     │     │        │  │  │  ├── test_abc.py
   │  │  │     │     │        │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  ├── test_argparse.py
   │  │  │     │     │        │  │  │  ├── test_arraymethod.py
   │  │  │     │     │        │  │  │  ├── test_arrayobject.py
   │  │  │     │     │        │  │  │  ├── test_arrayprint.py
   │  │  │     │     │        │  │  │  ├── test_array_api_info.py
   │  │  │     │     │        │  │  │  ├── test_array_coercion.py
   │  │  │     │     │        │  │  │  ├── test_array_interface.py
   │  │  │     │     │        │  │  │  ├── test_casting_floatingpoint_errors.py
   │  │  │     │     │        │  │  │  ├── test_casting_unittests.py
   │  │  │     │     │        │  │  │  ├── test_conversion_utils.py
   │  │  │     │     │        │  │  │  ├── test_cpu_dispatcher.py
   │  │  │     │     │        │  │  │  ├── test_cpu_features.py
   │  │  │     │     │        │  │  │  ├── test_custom_dtypes.py
   │  │  │     │     │        │  │  │  ├── test_cython.py
   │  │  │     │     │        │  │  │  ├── test_datetime.py
   │  │  │     │     │        │  │  │  ├── test_defchararray.py
   │  │  │     │     │        │  │  │  ├── test_deprecations.py
   │  │  │     │     │        │  │  │  ├── test_dlpack.py
   │  │  │     │     │        │  │  │  ├── test_dtype.py
   │  │  │     │     │        │  │  │  ├── test_einsum.py
   │  │  │     │     │        │  │  │  ├── test_errstate.py
   │  │  │     │     │        │  │  │  ├── test_extint128.py
   │  │  │     │     │        │  │  │  ├── test_function_base.py
   │  │  │     │     │        │  │  │  ├── test_getlimits.py
   │  │  │     │     │        │  │  │  ├── test_half.py
   │  │  │     │     │        │  │  │  ├── test_hashtable.py
   │  │  │     │     │        │  │  │  ├── test_indexerrors.py
   │  │  │     │     │        │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  ├── test_item_selection.py
   │  │  │     │     │        │  │  │  ├── test_limited_api.py
   │  │  │     │     │        │  │  │  ├── test_longdouble.py
   │  │  │     │     │        │  │  │  ├── test_machar.py
   │  │  │     │     │        │  │  │  ├── test_memmap.py
   │  │  │     │     │        │  │  │  ├── test_mem_overlap.py
   │  │  │     │     │        │  │  │  ├── test_mem_policy.py
   │  │  │     │     │        │  │  │  ├── test_multiarray.py
   │  │  │     │     │        │  │  │  ├── test_multithreading.py
   │  │  │     │     │        │  │  │  ├── test_nditer.py
   │  │  │     │     │        │  │  │  ├── test_nep50_promotions.py
   │  │  │     │     │        │  │  │  ├── test_numeric.py
   │  │  │     │     │        │  │  │  ├── test_numerictypes.py
   │  │  │     │     │        │  │  │  ├── test_overrides.py
   │  │  │     │     │        │  │  │  ├── test_print.py
   │  │  │     │     │        │  │  │  ├── test_protocols.py
   │  │  │     │     │        │  │  │  ├── test_records.py
   │  │  │     │     │        │  │  │  ├── test_regression.py
   │  │  │     │     │        │  │  │  ├── test_scalarbuffer.py
   │  │  │     │     │        │  │  │  ├── test_scalarinherit.py
   │  │  │     │     │        │  │  │  ├── test_scalarmath.py
   │  │  │     │     │        │  │  │  ├── test_scalarprint.py
   │  │  │     │     │        │  │  │  ├── test_scalar_ctors.py
   │  │  │     │     │        │  │  │  ├── test_scalar_methods.py
   │  │  │     │     │        │  │  │  ├── test_shape_base.py
   │  │  │     │     │        │  │  │  ├── test_simd.py
   │  │  │     │     │        │  │  │  ├── test_simd_module.py
   │  │  │     │     │        │  │  │  ├── test_stringdtype.py
   │  │  │     │     │        │  │  │  ├── test_strings.py
   │  │  │     │     │        │  │  │  ├── test_ufunc.py
   │  │  │     │     │        │  │  │  ├── test_umath.py
   │  │  │     │     │        │  │  │  ├── test_umath_accuracy.py
   │  │  │     │     │        │  │  │  ├── test_umath_complex.py
   │  │  │     │     │        │  │  │  ├── test_unicode.py
   │  │  │     │     │        │  │  │  ├── test__exceptions.py
   │  │  │     │     │        │  │  │  ├── _locales.py
   │  │  │     │     │        │  │  │  └── _natype.py
   │  │  │     │     │        │  │  ├── umath.py
   │  │  │     │     │        │  │  ├── umath.pyi
   │  │  │     │     │        │  │  ├── _add_newdocs.py
   │  │  │     │     │        │  │  ├── _add_newdocs.pyi
   │  │  │     │     │        │  │  ├── _add_newdocs_scalars.py
   │  │  │     │     │        │  │  ├── _add_newdocs_scalars.pyi
   │  │  │     │     │        │  │  ├── _asarray.py
   │  │  │     │     │        │  │  ├── _asarray.pyi
   │  │  │     │     │        │  │  ├── _dtype.py
   │  │  │     │     │        │  │  ├── _dtype.pyi
   │  │  │     │     │        │  │  ├── _dtype_ctypes.py
   │  │  │     │     │        │  │  ├── _dtype_ctypes.pyi
   │  │  │     │     │        │  │  ├── _exceptions.py
   │  │  │     │     │        │  │  ├── _exceptions.pyi
   │  │  │     │     │        │  │  ├── _internal.py
   │  │  │     │     │        │  │  ├── _internal.pyi
   │  │  │     │     │        │  │  ├── _machar.py
   │  │  │     │     │        │  │  ├── _machar.pyi
   │  │  │     │     │        │  │  ├── _methods.py
   │  │  │     │     │        │  │  ├── _methods.pyi
   │  │  │     │     │        │  │  ├── _multiarray_tests.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _multiarray_umath.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _operand_flag_tests.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _rational_tests.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _simd.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _simd.pyi
   │  │  │     │     │        │  │  ├── _string_helpers.py
   │  │  │     │     │        │  │  ├── _string_helpers.pyi
   │  │  │     │     │        │  │  ├── _struct_ufunc_tests.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── _type_aliases.py
   │  │  │     │     │        │  │  ├── _type_aliases.pyi
   │  │  │     │     │        │  │  ├── _ufunc_config.py
   │  │  │     │     │        │  │  ├── _ufunc_config.pyi
   │  │  │     │     │        │  │  ├── _umath_tests.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── _distributor_init.py
   │  │  │     │     │        │  ├── _distributor_init.pyi
   │  │  │     │     │        │  ├── _expired_attrs_2_0.py
   │  │  │     │     │        │  ├── _expired_attrs_2_0.pyi
   │  │  │     │     │        │  ├── _globals.py
   │  │  │     │     │        │  ├── _globals.pyi
   │  │  │     │     │        │  ├── _pyinstaller
   │  │  │     │     │        │  │  ├── hook-numpy.py
   │  │  │     │     │        │  │  ├── hook-numpy.pyi
   │  │  │     │     │        │  │  ├── tests
   │  │  │     │     │        │  │  │  ├── pyinstaller-smoke.py
   │  │  │     │     │        │  │  │  ├── test_pyinstaller.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── _pytesttester.py
   │  │  │     │     │        │  ├── _pytesttester.pyi
   │  │  │     │     │        │  ├── _typing
   │  │  │     │     │        │  │  ├── _add_docstring.py
   │  │  │     │     │        │  │  ├── _array_like.py
   │  │  │     │     │        │  │  ├── _char_codes.py
   │  │  │     │     │        │  │  ├── _dtype_like.py
   │  │  │     │     │        │  │  ├── _extended_precision.py
   │  │  │     │     │        │  │  ├── _nbit.py
   │  │  │     │     │        │  │  ├── _nbit_base.py
   │  │  │     │     │        │  │  ├── _nbit_base.pyi
   │  │  │     │     │        │  │  ├── _nested_sequence.py
   │  │  │     │     │        │  │  ├── _scalars.py
   │  │  │     │     │        │  │  ├── _shape.py
   │  │  │     │     │        │  │  ├── _ufunc.py
   │  │  │     │     │        │  │  ├── _ufunc.pyi
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── _utils
   │  │  │     │     │        │  │  ├── _convertions.py
   │  │  │     │     │        │  │  ├── _convertions.pyi
   │  │  │     │     │        │  │  ├── _inspect.py
   │  │  │     │     │        │  │  ├── _inspect.pyi
   │  │  │     │     │        │  │  ├── _pep440.py
   │  │  │     │     │        │  │  ├── _pep440.pyi
   │  │  │     │     │        │  │  ├── __init__.py
   │  │  │     │     │        │  │  └── __init__.pyi
   │  │  │     │     │        │  ├── __config__.py
   │  │  │     │     │        │  ├── __config__.pyi
   │  │  │     │     │        │  ├── __init__.cython-30.pxd
   │  │  │     │     │        │  ├── __init__.pxd
   │  │  │     │     │        │  ├── __init__.py
   │  │  │     │     │        │  └── __init__.pyi
   │  │  │     │     │       ├── numpy-2.3.4.dist-info
   │  │  │     │     │        │  ├── entry_points.txt
   │  │  │     │     │        │  ├── INSTALLER
   │  │  │     │     │        │  ├── LICENSE.txt
   │  │  │     │     │        │  ├── METADATA
   │  │  │     │     │        │  ├── RECORD
   │  │  │     │     │        │  └── WHEEL
   │  │  │     │     │       ├── numpy.libs
   │  │  │     │     │        │  ├── libgfortran-040039e1-0352e75f.so.5.0.0
   │  │  │     │     │        │  ├── libquadmath-96973f99-934c22de.so.0.0.0
   │  │  │     │     │        │  └── libscipy_openblas64_-8fb3d286.so
   │  │  │     │     │       ├── pandas
   │  │  │     │     │        │  ├── api
   │  │  │     │     │        │  │  ├── extensions
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── indexers
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── interchange
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── types
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── typing
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── arrays
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── compat
   │  │  │     │     │        │  │  ├── compressors.py
   │  │  │     │     │        │  │  ├── numpy
   │  │  │     │     │        │  │  │  ├── function.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── pickle_compat.py
   │  │  │     │     │        │  │  ├── pyarrow.py
   │  │  │     │     │        │  │  ├── _constants.py
   │  │  │     │     │        │  │  ├── _optional.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── conftest.py
   │  │  │     │     │        │  ├── core
   │  │  │     │     │        │  │  ├── accessor.py
   │  │  │     │     │        │  │  ├── algorithms.py
   │  │  │     │     │        │  │  ├── api.py
   │  │  │     │     │        │  │  ├── apply.py
   │  │  │     │     │        │  │  ├── arraylike.py
   │  │  │     │     │        │  │  ├── arrays
   │  │  │     │     │        │  │  │  ├── arrow
   │  │  │     │     │        │  │  │  │  ├── accessors.py
   │  │  │     │     │        │  │  │  │  ├── array.py
   │  │  │     │     │        │  │  │  │  ├── extension_types.py
   │  │  │     │     │        │  │  │  │  ├── _arrow_utils.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── boolean.py
   │  │  │     │     │        │  │  │  ├── categorical.py
   │  │  │     │     │        │  │  │  ├── datetimelike.py
   │  │  │     │     │        │  │  │  ├── datetimes.py
   │  │  │     │     │        │  │  │  ├── floating.py
   │  │  │     │     │        │  │  │  ├── integer.py
   │  │  │     │     │        │  │  │  ├── interval.py
   │  │  │     │     │        │  │  │  ├── masked.py
   │  │  │     │     │        │  │  │  ├── numeric.py
   │  │  │     │     │        │  │  │  ├── numpy_.py
   │  │  │     │     │        │  │  │  ├── period.py
   │  │  │     │     │        │  │  │  ├── sparse
   │  │  │     │     │        │  │  │  │  ├── accessor.py
   │  │  │     │     │        │  │  │  │  ├── array.py
   │  │  │     │     │        │  │  │  │  ├── scipy_sparse.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── string_.py
   │  │  │     │     │        │  │  │  ├── string_arrow.py
   │  │  │     │     │        │  │  │  ├── timedeltas.py
   │  │  │     │     │        │  │  │  ├── _arrow_string_mixins.py
   │  │  │     │     │        │  │  │  ├── _mixins.py
   │  │  │     │     │        │  │  │  ├── _ranges.py
   │  │  │     │     │        │  │  │  ├── _utils.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── array_algos
   │  │  │     │     │        │  │  │  ├── datetimelike_accumulations.py
   │  │  │     │     │        │  │  │  ├── masked_accumulations.py
   │  │  │     │     │        │  │  │  ├── masked_reductions.py
   │  │  │     │     │        │  │  │  ├── putmask.py
   │  │  │     │     │        │  │  │  ├── quantile.py
   │  │  │     │     │        │  │  │  ├── replace.py
   │  │  │     │     │        │  │  │  ├── take.py
   │  │  │     │     │        │  │  │  ├── transforms.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── base.py
   │  │  │     │     │        │  │  ├── common.py
   │  │  │     │     │        │  │  ├── computation
   │  │  │     │     │        │  │  │  ├── align.py
   │  │  │     │     │        │  │  │  ├── api.py
   │  │  │     │     │        │  │  │  ├── check.py
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── engines.py
   │  │  │     │     │        │  │  │  ├── eval.py
   │  │  │     │     │        │  │  │  ├── expr.py
   │  │  │     │     │        │  │  │  ├── expressions.py
   │  │  │     │     │        │  │  │  ├── ops.py
   │  │  │     │     │        │  │  │  ├── parsing.py
   │  │  │     │     │        │  │  │  ├── pytables.py
   │  │  │     │     │        │  │  │  ├── scope.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── config_init.py
   │  │  │     │     │        │  │  ├── construction.py
   │  │  │     │     │        │  │  ├── dtypes
   │  │  │     │     │        │  │  │  ├── api.py
   │  │  │     │     │        │  │  │  ├── astype.py
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── cast.py
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── concat.py
   │  │  │     │     │        │  │  │  ├── dtypes.py
   │  │  │     │     │        │  │  │  ├── generic.py
   │  │  │     │     │        │  │  │  ├── inference.py
   │  │  │     │     │        │  │  │  ├── missing.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── flags.py
   │  │  │     │     │        │  │  ├── frame.py
   │  │  │     │     │        │  │  ├── generic.py
   │  │  │     │     │        │  │  ├── groupby
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── categorical.py
   │  │  │     │     │        │  │  │  ├── generic.py
   │  │  │     │     │        │  │  │  ├── groupby.py
   │  │  │     │     │        │  │  │  ├── grouper.py
   │  │  │     │     │        │  │  │  ├── indexing.py
   │  │  │     │     │        │  │  │  ├── numba_.py
   │  │  │     │     │        │  │  │  ├── ops.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── indexers
   │  │  │     │     │        │  │  │  ├── objects.py
   │  │  │     │     │        │  │  │  ├── utils.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── indexes
   │  │  │     │     │        │  │  │  ├── accessors.py
   │  │  │     │     │        │  │  │  ├── api.py
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── category.py
   │  │  │     │     │        │  │  │  ├── datetimelike.py
   │  │  │     │     │        │  │  │  ├── datetimes.py
   │  │  │     │     │        │  │  │  ├── extension.py
   │  │  │     │     │        │  │  │  ├── frozen.py
   │  │  │     │     │        │  │  │  ├── interval.py
   │  │  │     │     │        │  │  │  ├── multi.py
   │  │  │     │     │        │  │  │  ├── period.py
   │  │  │     │     │        │  │  │  ├── range.py
   │  │  │     │     │        │  │  │  ├── timedeltas.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── indexing.py
   │  │  │     │     │        │  │  ├── interchange
   │  │  │     │     │        │  │  │  ├── buffer.py
   │  │  │     │     │        │  │  │  ├── column.py
   │  │  │     │     │        │  │  │  ├── dataframe.py
   │  │  │     │     │        │  │  │  ├── dataframe_protocol.py
   │  │  │     │     │        │  │  │  ├── from_dataframe.py
   │  │  │     │     │        │  │  │  ├── utils.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── internals
   │  │  │     │     │        │  │  │  ├── api.py
   │  │  │     │     │        │  │  │  ├── array_manager.py
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── blocks.py
   │  │  │     │     │        │  │  │  ├── concat.py
   │  │  │     │     │        │  │  │  ├── construction.py
   │  │  │     │     │        │  │  │  ├── managers.py
   │  │  │     │     │        │  │  │  ├── ops.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── methods
   │  │  │     │     │        │  │  │  ├── describe.py
   │  │  │     │     │        │  │  │  ├── selectn.py
   │  │  │     │     │        │  │  │  ├── to_dict.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── missing.py
   │  │  │     │     │        │  │  ├── nanops.py
   │  │  │     │     │        │  │  ├── ops
   │  │  │     │     │        │  │  │  ├── array_ops.py
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── dispatch.py
   │  │  │     │     │        │  │  │  ├── docstrings.py
   │  │  │     │     │        │  │  │  ├── invalid.py
   │  │  │     │     │        │  │  │  ├── mask_ops.py
   │  │  │     │     │        │  │  │  ├── missing.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── resample.py
   │  │  │     │     │        │  │  ├── reshape
   │  │  │     │     │        │  │  │  ├── api.py
   │  │  │     │     │        │  │  │  ├── concat.py
   │  │  │     │     │        │  │  │  ├── encoding.py
   │  │  │     │     │        │  │  │  ├── melt.py
   │  │  │     │     │        │  │  │  ├── merge.py
   │  │  │     │     │        │  │  │  ├── pivot.py
   │  │  │     │     │        │  │  │  ├── reshape.py
   │  │  │     │     │        │  │  │  ├── tile.py
   │  │  │     │     │        │  │  │  ├── util.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── roperator.py
   │  │  │     │     │        │  │  ├── sample.py
   │  │  │     │     │        │  │  ├── series.py
   │  │  │     │     │        │  │  ├── shared_docs.py
   │  │  │     │     │        │  │  ├── sorting.py
   │  │  │     │     │        │  │  ├── sparse
   │  │  │     │     │        │  │  │  ├── api.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── strings
   │  │  │     │     │        │  │  │  ├── accessor.py
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── object_array.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── tools
   │  │  │     │     │        │  │  │  ├── datetimes.py
   │  │  │     │     │        │  │  │  ├── numeric.py
   │  │  │     │     │        │  │  │  ├── timedeltas.py
   │  │  │     │     │        │  │  │  ├── times.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── util
   │  │  │     │     │        │  │  │  ├── hashing.py
   │  │  │     │     │        │  │  │  ├── numba_.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── window
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── doc.py
   │  │  │     │     │        │  │  │  ├── ewm.py
   │  │  │     │     │        │  │  │  ├── expanding.py
   │  │  │     │     │        │  │  │  ├── numba_.py
   │  │  │     │     │        │  │  │  ├── online.py
   │  │  │     │     │        │  │  │  ├── rolling.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── _numba
   │  │  │     │     │        │  │  │  ├── executor.py
   │  │  │     │     │        │  │  │  ├── extensions.py
   │  │  │     │     │        │  │  │  ├── kernels
   │  │  │     │     │        │  │  │  │  ├── mean_.py
   │  │  │     │     │        │  │  │  │  ├── min_max_.py
   │  │  │     │     │        │  │  │  │  ├── shared.py
   │  │  │     │     │        │  │  │  │  ├── sum_.py
   │  │  │     │     │        │  │  │  │  ├── var_.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── errors
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── io
   │  │  │     │     │        │  │  ├── api.py
   │  │  │     │     │        │  │  ├── clipboard
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── clipboards.py
   │  │  │     │     │        │  │  ├── common.py
   │  │  │     │     │        │  │  ├── excel
   │  │  │     │     │        │  │  │  ├── _base.py
   │  │  │     │     │        │  │  │  ├── _calamine.py
   │  │  │     │     │        │  │  │  ├── _odfreader.py
   │  │  │     │     │        │  │  │  ├── _odswriter.py
   │  │  │     │     │        │  │  │  ├── _openpyxl.py
   │  │  │     │     │        │  │  │  ├── _pyxlsb.py
   │  │  │     │     │        │  │  │  ├── _util.py
   │  │  │     │     │        │  │  │  ├── _xlrd.py
   │  │  │     │     │        │  │  │  ├── _xlsxwriter.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── feather_format.py
   │  │  │     │     │        │  │  ├── formats
   │  │  │     │     │        │  │  │  ├── console.py
   │  │  │     │     │        │  │  │  ├── css.py
   │  │  │     │     │        │  │  │  ├── csvs.py
   │  │  │     │     │        │  │  │  ├── excel.py
   │  │  │     │     │        │  │  │  ├── format.py
   │  │  │     │     │        │  │  │  ├── html.py
   │  │  │     │     │        │  │  │  ├── info.py
   │  │  │     │     │        │  │  │  ├── printing.py
   │  │  │     │     │        │  │  │  ├── string.py
   │  │  │     │     │        │  │  │  ├── style.py
   │  │  │     │     │        │  │  │  ├── style_render.py
   │  │  │     │     │        │  │  │  ├── templates
   │  │  │     │     │        │  │  │  │  ├── html.tpl
   │  │  │     │     │        │  │  │  │  ├── html_style.tpl
   │  │  │     │     │        │  │  │  │  ├── html_table.tpl
   │  │  │     │     │        │  │  │  │  ├── latex.tpl
   │  │  │     │     │        │  │  │  │  ├── latex_longtable.tpl
   │  │  │     │     │        │  │  │  │  ├── latex_table.tpl
   │  │  │     │     │        │  │  │  │  └── string.tpl
   │  │  │     │     │        │  │  │  ├── xml.py
   │  │  │     │     │        │  │  │  ├── _color_data.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── gbq.py
   │  │  │     │     │        │  │  ├── html.py
   │  │  │     │     │        │  │  ├── json
   │  │  │     │     │        │  │  │  ├── _json.py
   │  │  │     │     │        │  │  │  ├── _normalize.py
   │  │  │     │     │        │  │  │  ├── _table_schema.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── orc.py
   │  │  │     │     │        │  │  ├── parquet.py
   │  │  │     │     │        │  │  ├── parsers
   │  │  │     │     │        │  │  │  ├── arrow_parser_wrapper.py
   │  │  │     │     │        │  │  │  ├── base_parser.py
   │  │  │     │     │        │  │  │  ├── c_parser_wrapper.py
   │  │  │     │     │        │  │  │  ├── python_parser.py
   │  │  │     │     │        │  │  │  ├── readers.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── pickle.py
   │  │  │     │     │        │  │  ├── pytables.py
   │  │  │     │     │        │  │  ├── sas
   │  │  │     │     │        │  │  │  ├── sas7bdat.py
   │  │  │     │     │        │  │  │  ├── sasreader.py
   │  │  │     │     │        │  │  │  ├── sas_constants.py
   │  │  │     │     │        │  │  │  ├── sas_xport.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── spss.py
   │  │  │     │     │        │  │  ├── sql.py
   │  │  │     │     │        │  │  ├── stata.py
   │  │  │     │     │        │  │  ├── xml.py
   │  │  │     │     │        │  │  ├── _util.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── plotting
   │  │  │     │     │        │  │  ├── _core.py
   │  │  │     │     │        │  │  ├── _matplotlib
   │  │  │     │     │        │  │  │  ├── boxplot.py
   │  │  │     │     │        │  │  │  ├── converter.py
   │  │  │     │     │        │  │  │  ├── core.py
   │  │  │     │     │        │  │  │  ├── groupby.py
   │  │  │     │     │        │  │  │  ├── hist.py
   │  │  │     │     │        │  │  │  ├── misc.py
   │  │  │     │     │        │  │  │  ├── style.py
   │  │  │     │     │        │  │  │  ├── timeseries.py
   │  │  │     │     │        │  │  │  ├── tools.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── _misc.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── pyproject.toml
   │  │  │     │     │        │  ├── testing.py
   │  │  │     │     │        │  ├── tests
   │  │  │     │     │        │  │  ├── api
   │  │  │     │     │        │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  ├── test_types.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── apply
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── test_frame_apply.py
   │  │  │     │     │        │  │  │  ├── test_frame_apply_relabeling.py
   │  │  │     │     │        │  │  │  ├── test_frame_transform.py
   │  │  │     │     │        │  │  │  ├── test_invalid_arg.py
   │  │  │     │     │        │  │  │  ├── test_numba.py
   │  │  │     │     │        │  │  │  ├── test_series_apply.py
   │  │  │     │     │        │  │  │  ├── test_series_apply_relabeling.py
   │  │  │     │     │        │  │  │  ├── test_series_transform.py
   │  │  │     │     │        │  │  │  ├── test_str.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── arithmetic
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── test_array_ops.py
   │  │  │     │     │        │  │  │  ├── test_categorical.py
   │  │  │     │     │        │  │  │  ├── test_datetime64.py
   │  │  │     │     │        │  │  │  ├── test_interval.py
   │  │  │     │     │        │  │  │  ├── test_numeric.py
   │  │  │     │     │        │  │  │  ├── test_object.py
   │  │  │     │     │        │  │  │  ├── test_period.py
   │  │  │     │     │        │  │  │  ├── test_timedelta64.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── arrays
   │  │  │     │     │        │  │  │  ├── boolean
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_comparison.py
   │  │  │     │     │        │  │  │  │  ├── test_construction.py
   │  │  │     │     │        │  │  │  │  ├── test_function.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_logical.py
   │  │  │     │     │        │  │  │  │  ├── test_ops.py
   │  │  │     │     │        │  │  │  │  ├── test_reduction.py
   │  │  │     │     │        │  │  │  │  ├── test_repr.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── categorical
   │  │  │     │     │        │  │  │  │  ├── test_algos.py
   │  │  │     │     │        │  │  │  │  ├── test_analytics.py
   │  │  │     │     │        │  │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_dtypes.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_map.py
   │  │  │     │     │        │  │  │  │  ├── test_missing.py
   │  │  │     │     │        │  │  │  │  ├── test_operators.py
   │  │  │     │     │        │  │  │  │  ├── test_replace.py
   │  │  │     │     │        │  │  │  │  ├── test_repr.py
   │  │  │     │     │        │  │  │  │  ├── test_sorting.py
   │  │  │     │     │        │  │  │  │  ├── test_subclass.py
   │  │  │     │     │        │  │  │  │  ├── test_take.py
   │  │  │     │     │        │  │  │  │  ├── test_warnings.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── datetimes
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_cumulative.py
   │  │  │     │     │        │  │  │  │  ├── test_reductions.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── floating
   │  │  │     │     │        │  │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_comparison.py
   │  │  │     │     │        │  │  │  │  ├── test_concat.py
   │  │  │     │     │        │  │  │  │  ├── test_construction.py
   │  │  │     │     │        │  │  │  │  ├── test_contains.py
   │  │  │     │     │        │  │  │  │  ├── test_function.py
   │  │  │     │     │        │  │  │  │  ├── test_repr.py
   │  │  │     │     │        │  │  │  │  ├── test_to_numpy.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── integer
   │  │  │     │     │        │  │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_comparison.py
   │  │  │     │     │        │  │  │  │  ├── test_concat.py
   │  │  │     │     │        │  │  │  │  ├── test_construction.py
   │  │  │     │     │        │  │  │  │  ├── test_dtypes.py
   │  │  │     │     │        │  │  │  │  ├── test_function.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_reduction.py
   │  │  │     │     │        │  │  │  │  ├── test_repr.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── interval
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_interval.py
   │  │  │     │     │        │  │  │  │  ├── test_interval_pyarrow.py
   │  │  │     │     │        │  │  │  │  ├── test_overlaps.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── masked
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_arrow_compat.py
   │  │  │     │     │        │  │  │  │  ├── test_function.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── masked_shared.py
   │  │  │     │     │        │  │  │  ├── numpy_
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_numpy.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── period
   │  │  │     │     │        │  │  │  │  ├── test_arrow_compat.py
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_reductions.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── sparse
   │  │  │     │     │        │  │  │  │  ├── test_accessor.py
   │  │  │     │     │        │  │  │  │  ├── test_arithmetics.py
   │  │  │     │     │        │  │  │  │  ├── test_array.py
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_combine_concat.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_dtype.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_libsparse.py
   │  │  │     │     │        │  │  │  │  ├── test_reductions.py
   │  │  │     │     │        │  │  │  │  ├── test_unary.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── string_
   │  │  │     │     │        │  │  │  │  ├── test_concat.py
   │  │  │     │     │        │  │  │  │  ├── test_string.py
   │  │  │     │     │        │  │  │  │  ├── test_string_arrow.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_array.py
   │  │  │     │     │        │  │  │  ├── test_datetimelike.py
   │  │  │     │     │        │  │  │  ├── test_datetimes.py
   │  │  │     │     │        │  │  │  ├── test_ndarray_backed.py
   │  │  │     │     │        │  │  │  ├── test_period.py
   │  │  │     │     │        │  │  │  ├── test_timedeltas.py
   │  │  │     │     │        │  │  │  ├── timedeltas
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_cumulative.py
   │  │  │     │     │        │  │  │  │  ├── test_reductions.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── base
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  ├── test_conversion.py
   │  │  │     │     │        │  │  │  ├── test_fillna.py
   │  │  │     │     │        │  │  │  ├── test_misc.py
   │  │  │     │     │        │  │  │  ├── test_transpose.py
   │  │  │     │     │        │  │  │  ├── test_unique.py
   │  │  │     │     │        │  │  │  ├── test_value_counts.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── computation
   │  │  │     │     │        │  │  │  ├── test_compat.py
   │  │  │     │     │        │  │  │  ├── test_eval.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── config
   │  │  │     │     │        │  │  │  ├── test_config.py
   │  │  │     │     │        │  │  │  ├── test_localization.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── construction
   │  │  │     │     │        │  │  │  ├── test_extract_array.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── copy_view
   │  │  │     │     │        │  │  │  ├── index
   │  │  │     │     │        │  │  │  │  ├── test_datetimeindex.py
   │  │  │     │     │        │  │  │  │  ├── test_index.py
   │  │  │     │     │        │  │  │  │  ├── test_periodindex.py
   │  │  │     │     │        │  │  │  │  ├── test_timedeltaindex.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_array.py
   │  │  │     │     │        │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  ├── test_chained_assignment_deprecation.py
   │  │  │     │     │        │  │  │  ├── test_clip.py
   │  │  │     │     │        │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  ├── test_core_functionalities.py
   │  │  │     │     │        │  │  │  ├── test_functions.py
   │  │  │     │     │        │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  ├── test_internals.py
   │  │  │     │     │        │  │  │  ├── test_interp_fillna.py
   │  │  │     │     │        │  │  │  ├── test_methods.py
   │  │  │     │     │        │  │  │  ├── test_replace.py
   │  │  │     │     │        │  │  │  ├── test_setitem.py
   │  │  │     │     │        │  │  │  ├── test_util.py
   │  │  │     │     │        │  │  │  ├── util.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── dtypes
   │  │  │     │     │        │  │  │  ├── cast
   │  │  │     │     │        │  │  │  │  ├── test_can_hold_element.py
   │  │  │     │     │        │  │  │  │  ├── test_construct_from_scalar.py
   │  │  │     │     │        │  │  │  │  ├── test_construct_ndarray.py
   │  │  │     │     │        │  │  │  │  ├── test_construct_object_arr.py
   │  │  │     │     │        │  │  │  │  ├── test_dict_compat.py
   │  │  │     │     │        │  │  │  │  ├── test_downcast.py
   │  │  │     │     │        │  │  │  │  ├── test_find_common_type.py
   │  │  │     │     │        │  │  │  │  ├── test_infer_datetimelike.py
   │  │  │     │     │        │  │  │  │  ├── test_infer_dtype.py
   │  │  │     │     │        │  │  │  │  ├── test_maybe_box_native.py
   │  │  │     │     │        │  │  │  │  ├── test_promote.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_common.py
   │  │  │     │     │        │  │  │  ├── test_concat.py
   │  │  │     │     │        │  │  │  ├── test_dtypes.py
   │  │  │     │     │        │  │  │  ├── test_generic.py
   │  │  │     │     │        │  │  │  ├── test_inference.py
   │  │  │     │     │        │  │  │  ├── test_missing.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── extension
   │  │  │     │     │        │  │  │  ├── array_with_attr
   │  │  │     │     │        │  │  │  │  ├── array.py
   │  │  │     │     │        │  │  │  │  ├── test_array_with_attr.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── base
   │  │  │     │     │        │  │  │  │  ├── accumulate.py
   │  │  │     │     │        │  │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  │  ├── casting.py
   │  │  │     │     │        │  │  │  │  ├── constructors.py
   │  │  │     │     │        │  │  │  │  ├── dim2.py
   │  │  │     │     │        │  │  │  │  ├── dtype.py
   │  │  │     │     │        │  │  │  │  ├── getitem.py
   │  │  │     │     │        │  │  │  │  ├── groupby.py
   │  │  │     │     │        │  │  │  │  ├── index.py
   │  │  │     │     │        │  │  │  │  ├── interface.py
   │  │  │     │     │        │  │  │  │  ├── io.py
   │  │  │     │     │        │  │  │  │  ├── methods.py
   │  │  │     │     │        │  │  │  │  ├── missing.py
   │  │  │     │     │        │  │  │  │  ├── ops.py
   │  │  │     │     │        │  │  │  │  ├── printing.py
   │  │  │     │     │        │  │  │  │  ├── reduce.py
   │  │  │     │     │        │  │  │  │  ├── reshaping.py
   │  │  │     │     │        │  │  │  │  ├── setitem.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── date
   │  │  │     │     │        │  │  │  │  ├── array.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── decimal
   │  │  │     │     │        │  │  │  │  ├── array.py
   │  │  │     │     │        │  │  │  │  ├── test_decimal.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── json
   │  │  │     │     │        │  │  │  │  ├── array.py
   │  │  │     │     │        │  │  │  │  ├── test_json.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── list
   │  │  │     │     │        │  │  │  │  ├── array.py
   │  │  │     │     │        │  │  │  │  ├── test_list.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_arrow.py
   │  │  │     │     │        │  │  │  ├── test_categorical.py
   │  │  │     │     │        │  │  │  ├── test_common.py
   │  │  │     │     │        │  │  │  ├── test_datetime.py
   │  │  │     │     │        │  │  │  ├── test_extension.py
   │  │  │     │     │        │  │  │  ├── test_interval.py
   │  │  │     │     │        │  │  │  ├── test_masked.py
   │  │  │     │     │        │  │  │  ├── test_numpy.py
   │  │  │     │     │        │  │  │  ├── test_period.py
   │  │  │     │     │        │  │  │  ├── test_sparse.py
   │  │  │     │     │        │  │  │  ├── test_string.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── frame
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── constructors
   │  │  │     │     │        │  │  │  │  ├── test_from_dict.py
   │  │  │     │     │        │  │  │  │  ├── test_from_records.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── indexing
   │  │  │     │     │        │  │  │  │  ├── test_coercion.py
   │  │  │     │     │        │  │  │  │  ├── test_delitem.py
   │  │  │     │     │        │  │  │  │  ├── test_get.py
   │  │  │     │     │        │  │  │  │  ├── test_getitem.py
   │  │  │     │     │        │  │  │  │  ├── test_get_value.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_insert.py
   │  │  │     │     │        │  │  │  │  ├── test_mask.py
   │  │  │     │     │        │  │  │  │  ├── test_setitem.py
   │  │  │     │     │        │  │  │  │  ├── test_set_value.py
   │  │  │     │     │        │  │  │  │  ├── test_take.py
   │  │  │     │     │        │  │  │  │  ├── test_where.py
   │  │  │     │     │        │  │  │  │  ├── test_xs.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── methods
   │  │  │     │     │        │  │  │  │  ├── test_add_prefix_suffix.py
   │  │  │     │     │        │  │  │  │  ├── test_align.py
   │  │  │     │     │        │  │  │  │  ├── test_asfreq.py
   │  │  │     │     │        │  │  │  │  ├── test_asof.py
   │  │  │     │     │        │  │  │  │  ├── test_assign.py
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_at_time.py
   │  │  │     │     │        │  │  │  │  ├── test_between_time.py
   │  │  │     │     │        │  │  │  │  ├── test_clip.py
   │  │  │     │     │        │  │  │  │  ├── test_combine.py
   │  │  │     │     │        │  │  │  │  ├── test_combine_first.py
   │  │  │     │     │        │  │  │  │  ├── test_compare.py
   │  │  │     │     │        │  │  │  │  ├── test_convert_dtypes.py
   │  │  │     │     │        │  │  │  │  ├── test_copy.py
   │  │  │     │     │        │  │  │  │  ├── test_count.py
   │  │  │     │     │        │  │  │  │  ├── test_cov_corr.py
   │  │  │     │     │        │  │  │  │  ├── test_describe.py
   │  │  │     │     │        │  │  │  │  ├── test_diff.py
   │  │  │     │     │        │  │  │  │  ├── test_dot.py
   │  │  │     │     │        │  │  │  │  ├── test_drop.py
   │  │  │     │     │        │  │  │  │  ├── test_droplevel.py
   │  │  │     │     │        │  │  │  │  ├── test_dropna.py
   │  │  │     │     │        │  │  │  │  ├── test_drop_duplicates.py
   │  │  │     │     │        │  │  │  │  ├── test_dtypes.py
   │  │  │     │     │        │  │  │  │  ├── test_duplicated.py
   │  │  │     │     │        │  │  │  │  ├── test_equals.py
   │  │  │     │     │        │  │  │  │  ├── test_explode.py
   │  │  │     │     │        │  │  │  │  ├── test_fillna.py
   │  │  │     │     │        │  │  │  │  ├── test_filter.py
   │  │  │     │     │        │  │  │  │  ├── test_first_and_last.py
   │  │  │     │     │        │  │  │  │  ├── test_first_valid_index.py
   │  │  │     │     │        │  │  │  │  ├── test_get_numeric_data.py
   │  │  │     │     │        │  │  │  │  ├── test_head_tail.py
   │  │  │     │     │        │  │  │  │  ├── test_infer_objects.py
   │  │  │     │     │        │  │  │  │  ├── test_info.py
   │  │  │     │     │        │  │  │  │  ├── test_interpolate.py
   │  │  │     │     │        │  │  │  │  ├── test_isetitem.py
   │  │  │     │     │        │  │  │  │  ├── test_isin.py
   │  │  │     │     │        │  │  │  │  ├── test_is_homogeneous_dtype.py
   │  │  │     │     │        │  │  │  │  ├── test_iterrows.py
   │  │  │     │     │        │  │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  │  ├── test_map.py
   │  │  │     │     │        │  │  │  │  ├── test_matmul.py
   │  │  │     │     │        │  │  │  │  ├── test_nlargest.py
   │  │  │     │     │        │  │  │  │  ├── test_pct_change.py
   │  │  │     │     │        │  │  │  │  ├── test_pipe.py
   │  │  │     │     │        │  │  │  │  ├── test_pop.py
   │  │  │     │     │        │  │  │  │  ├── test_quantile.py
   │  │  │     │     │        │  │  │  │  ├── test_rank.py
   │  │  │     │     │        │  │  │  │  ├── test_reindex.py
   │  │  │     │     │        │  │  │  │  ├── test_reindex_like.py
   │  │  │     │     │        │  │  │  │  ├── test_rename.py
   │  │  │     │     │        │  │  │  │  ├── test_rename_axis.py
   │  │  │     │     │        │  │  │  │  ├── test_reorder_levels.py
   │  │  │     │     │        │  │  │  │  ├── test_replace.py
   │  │  │     │     │        │  │  │  │  ├── test_reset_index.py
   │  │  │     │     │        │  │  │  │  ├── test_round.py
   │  │  │     │     │        │  │  │  │  ├── test_sample.py
   │  │  │     │     │        │  │  │  │  ├── test_select_dtypes.py
   │  │  │     │     │        │  │  │  │  ├── test_set_axis.py
   │  │  │     │     │        │  │  │  │  ├── test_set_index.py
   │  │  │     │     │        │  │  │  │  ├── test_shift.py
   │  │  │     │     │        │  │  │  │  ├── test_size.py
   │  │  │     │     │        │  │  │  │  ├── test_sort_index.py
   │  │  │     │     │        │  │  │  │  ├── test_sort_values.py
   │  │  │     │     │        │  │  │  │  ├── test_swapaxes.py
   │  │  │     │     │        │  │  │  │  ├── test_swaplevel.py
   │  │  │     │     │        │  │  │  │  ├── test_to_csv.py
   │  │  │     │     │        │  │  │  │  ├── test_to_dict.py
   │  │  │     │     │        │  │  │  │  ├── test_to_dict_of_blocks.py
   │  │  │     │     │        │  │  │  │  ├── test_to_numpy.py
   │  │  │     │     │        │  │  │  │  ├── test_to_period.py
   │  │  │     │     │        │  │  │  │  ├── test_to_records.py
   │  │  │     │     │        │  │  │  │  ├── test_to_timestamp.py
   │  │  │     │     │        │  │  │  │  ├── test_transpose.py
   │  │  │     │     │        │  │  │  │  ├── test_truncate.py
   │  │  │     │     │        │  │  │  │  ├── test_tz_convert.py
   │  │  │     │     │        │  │  │  │  ├── test_tz_localize.py
   │  │  │     │     │        │  │  │  │  ├── test_update.py
   │  │  │     │     │        │  │  │  │  ├── test_values.py
   │  │  │     │     │        │  │  │  │  ├── test_value_counts.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_alter_axes.py
   │  │  │     │     │        │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  ├── test_arrow_interface.py
   │  │  │     │     │        │  │  │  ├── test_block_internals.py
   │  │  │     │     │        │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  ├── test_cumulative.py
   │  │  │     │     │        │  │  │  ├── test_iteration.py
   │  │  │     │     │        │  │  │  ├── test_logical_ops.py
   │  │  │     │     │        │  │  │  ├── test_nonunique_indexes.py
   │  │  │     │     │        │  │  │  ├── test_npfuncs.py
   │  │  │     │     │        │  │  │  ├── test_query_eval.py
   │  │  │     │     │        │  │  │  ├── test_reductions.py
   │  │  │     │     │        │  │  │  ├── test_repr.py
   │  │  │     │     │        │  │  │  ├── test_stack_unstack.py
   │  │  │     │     │        │  │  │  ├── test_subclass.py
   │  │  │     │     │        │  │  │  ├── test_ufunc.py
   │  │  │     │     │        │  │  │  ├── test_unary.py
   │  │  │     │     │        │  │  │  ├── test_validate.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── generic
   │  │  │     │     │        │  │  │  ├── test_duplicate_labels.py
   │  │  │     │     │        │  │  │  ├── test_finalize.py
   │  │  │     │     │        │  │  │  ├── test_frame.py
   │  │  │     │     │        │  │  │  ├── test_generic.py
   │  │  │     │     │        │  │  │  ├── test_label_or_level_utils.py
   │  │  │     │     │        │  │  │  ├── test_series.py
   │  │  │     │     │        │  │  │  ├── test_to_xarray.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── groupby
   │  │  │     │     │        │  │  │  ├── aggregate
   │  │  │     │     │        │  │  │  │  ├── test_aggregate.py
   │  │  │     │     │        │  │  │  │  ├── test_cython.py
   │  │  │     │     │        │  │  │  │  ├── test_numba.py
   │  │  │     │     │        │  │  │  │  ├── test_other.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── methods
   │  │  │     │     │        │  │  │  │  ├── test_corrwith.py
   │  │  │     │     │        │  │  │  │  ├── test_describe.py
   │  │  │     │     │        │  │  │  │  ├── test_groupby_shift_diff.py
   │  │  │     │     │        │  │  │  │  ├── test_is_monotonic.py
   │  │  │     │     │        │  │  │  │  ├── test_nlargest_nsmallest.py
   │  │  │     │     │        │  │  │  │  ├── test_nth.py
   │  │  │     │     │        │  │  │  │  ├── test_quantile.py
   │  │  │     │     │        │  │  │  │  ├── test_rank.py
   │  │  │     │     │        │  │  │  │  ├── test_sample.py
   │  │  │     │     │        │  │  │  │  ├── test_size.py
   │  │  │     │     │        │  │  │  │  ├── test_skew.py
   │  │  │     │     │        │  │  │  │  ├── test_value_counts.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_all_methods.py
   │  │  │     │     │        │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  ├── test_apply.py
   │  │  │     │     │        │  │  │  ├── test_apply_mutate.py
   │  │  │     │     │        │  │  │  ├── test_bin_groupby.py
   │  │  │     │     │        │  │  │  ├── test_categorical.py
   │  │  │     │     │        │  │  │  ├── test_counting.py
   │  │  │     │     │        │  │  │  ├── test_cumulative.py
   │  │  │     │     │        │  │  │  ├── test_filters.py
   │  │  │     │     │        │  │  │  ├── test_groupby.py
   │  │  │     │     │        │  │  │  ├── test_groupby_dropna.py
   │  │  │     │     │        │  │  │  ├── test_groupby_subclass.py
   │  │  │     │     │        │  │  │  ├── test_grouping.py
   │  │  │     │     │        │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  ├── test_index_as_string.py
   │  │  │     │     │        │  │  │  ├── test_libgroupby.py
   │  │  │     │     │        │  │  │  ├── test_missing.py
   │  │  │     │     │        │  │  │  ├── test_numba.py
   │  │  │     │     │        │  │  │  ├── test_numeric_only.py
   │  │  │     │     │        │  │  │  ├── test_pipe.py
   │  │  │     │     │        │  │  │  ├── test_raises.py
   │  │  │     │     │        │  │  │  ├── test_reductions.py
   │  │  │     │     │        │  │  │  ├── test_timegrouper.py
   │  │  │     │     │        │  │  │  ├── transform
   │  │  │     │     │        │  │  │  │  ├── test_numba.py
   │  │  │     │     │        │  │  │  │  ├── test_transform.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── indexes
   │  │  │     │     │        │  │  │  ├── base_class
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_pickle.py
   │  │  │     │     │        │  │  │  │  ├── test_reshape.py
   │  │  │     │     │        │  │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  │  ├── test_where.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── categorical
   │  │  │     │     │        │  │  │  │  ├── test_append.py
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_category.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_equals.py
   │  │  │     │     │        │  │  │  │  ├── test_fillna.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_map.py
   │  │  │     │     │        │  │  │  │  ├── test_reindex.py
   │  │  │     │     │        │  │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── datetimelike_
   │  │  │     │     │        │  │  │  │  ├── test_drop_duplicates.py
   │  │  │     │     │        │  │  │  │  ├── test_equals.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_is_monotonic.py
   │  │  │     │     │        │  │  │  │  ├── test_nat.py
   │  │  │     │     │        │  │  │  │  ├── test_sort_values.py
   │  │  │     │     │        │  │  │  │  ├── test_value_counts.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── datetimes
   │  │  │     │     │        │  │  │  │  ├── methods
   │  │  │     │     │        │  │  │  │  │  ├── test_asof.py
   │  │  │     │     │        │  │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  │  ├── test_delete.py
   │  │  │     │     │        │  │  │  │  │  ├── test_factorize.py
   │  │  │     │     │        │  │  │  │  │  ├── test_fillna.py
   │  │  │     │     │        │  │  │  │  │  ├── test_insert.py
   │  │  │     │     │        │  │  │  │  │  ├── test_isocalendar.py
   │  │  │     │     │        │  │  │  │  │  ├── test_map.py
   │  │  │     │     │        │  │  │  │  │  ├── test_normalize.py
   │  │  │     │     │        │  │  │  │  │  ├── test_repeat.py
   │  │  │     │     │        │  │  │  │  │  ├── test_resolution.py
   │  │  │     │     │        │  │  │  │  │  ├── test_round.py
   │  │  │     │     │        │  │  │  │  │  ├── test_shift.py
   │  │  │     │     │        │  │  │  │  │  ├── test_snap.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_frame.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_julian_date.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_period.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_pydatetime.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_series.py
   │  │  │     │     │        │  │  │  │  │  ├── test_tz_convert.py
   │  │  │     │     │        │  │  │  │  │  ├── test_tz_localize.py
   │  │  │     │     │        │  │  │  │  │  ├── test_unique.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_datetime.py
   │  │  │     │     │        │  │  │  │  ├── test_date_range.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_freq_attr.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_iter.py
   │  │  │     │     │        │  │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  │  ├── test_npfuncs.py
   │  │  │     │     │        │  │  │  │  ├── test_ops.py
   │  │  │     │     │        │  │  │  │  ├── test_partial_slicing.py
   │  │  │     │     │        │  │  │  │  ├── test_pickle.py
   │  │  │     │     │        │  │  │  │  ├── test_reindex.py
   │  │  │     │     │        │  │  │  │  ├── test_scalar_compat.py
   │  │  │     │     │        │  │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  │  ├── test_timezones.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── interval
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_equals.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_interval.py
   │  │  │     │     │        │  │  │  │  ├── test_interval_range.py
   │  │  │     │     │        │  │  │  │  ├── test_interval_tree.py
   │  │  │     │     │        │  │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  │  ├── test_pickle.py
   │  │  │     │     │        │  │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── multi
   │  │  │     │     │        │  │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  │  ├── test_analytics.py
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_compat.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_conversion.py
   │  │  │     │     │        │  │  │  │  ├── test_copy.py
   │  │  │     │     │        │  │  │  │  ├── test_drop.py
   │  │  │     │     │        │  │  │  │  ├── test_duplicates.py
   │  │  │     │     │        │  │  │  │  ├── test_equivalence.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_get_level_values.py
   │  │  │     │     │        │  │  │  │  ├── test_get_set.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_integrity.py
   │  │  │     │     │        │  │  │  │  ├── test_isin.py
   │  │  │     │     │        │  │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  │  ├── test_lexsort.py
   │  │  │     │     │        │  │  │  │  ├── test_missing.py
   │  │  │     │     │        │  │  │  │  ├── test_monotonic.py
   │  │  │     │     │        │  │  │  │  ├── test_names.py
   │  │  │     │     │        │  │  │  │  ├── test_partial_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_pickle.py
   │  │  │     │     │        │  │  │  │  ├── test_reindex.py
   │  │  │     │     │        │  │  │  │  ├── test_reshape.py
   │  │  │     │     │        │  │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  │  ├── test_sorting.py
   │  │  │     │     │        │  │  │  │  ├── test_take.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── numeric
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  │  ├── test_numeric.py
   │  │  │     │     │        │  │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── object
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── period
   │  │  │     │     │        │  │  │  │  ├── methods
   │  │  │     │     │        │  │  │  │  │  ├── test_asfreq.py
   │  │  │     │     │        │  │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  │  ├── test_factorize.py
   │  │  │     │     │        │  │  │  │  │  ├── test_fillna.py
   │  │  │     │     │        │  │  │  │  │  ├── test_insert.py
   │  │  │     │     │        │  │  │  │  │  ├── test_is_full.py
   │  │  │     │     │        │  │  │  │  │  ├── test_repeat.py
   │  │  │     │     │        │  │  │  │  │  ├── test_shift.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_timestamp.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_freq_attr.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  │  ├── test_monotonic.py
   │  │  │     │     │        │  │  │  │  ├── test_partial_slicing.py
   │  │  │     │     │        │  │  │  │  ├── test_period.py
   │  │  │     │     │        │  │  │  │  ├── test_period_range.py
   │  │  │     │     │        │  │  │  │  ├── test_pickle.py
   │  │  │     │     │        │  │  │  │  ├── test_resolution.py
   │  │  │     │     │        │  │  │  │  ├── test_scalar_compat.py
   │  │  │     │     │        │  │  │  │  ├── test_searchsorted.py
   │  │  │     │     │        │  │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  │  ├── test_tools.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── ranges
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  │  ├── test_range.py
   │  │  │     │     │        │  │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── string
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_any_index.py
   │  │  │     │     │        │  │  │  ├── test_base.py
   │  │  │     │     │        │  │  │  ├── test_common.py
   │  │  │     │     │        │  │  │  ├── test_datetimelike.py
   │  │  │     │     │        │  │  │  ├── test_engines.py
   │  │  │     │     │        │  │  │  ├── test_frozen.py
   │  │  │     │     │        │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  ├── test_index_new.py
   │  │  │     │     │        │  │  │  ├── test_numpy_compat.py
   │  │  │     │     │        │  │  │  ├── test_old_base.py
   │  │  │     │     │        │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  ├── test_subclass.py
   │  │  │     │     │        │  │  │  ├── timedeltas
   │  │  │     │     │        │  │  │  │  ├── methods
   │  │  │     │     │        │  │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  │  ├── test_factorize.py
   │  │  │     │     │        │  │  │  │  │  ├── test_fillna.py
   │  │  │     │     │        │  │  │  │  │  ├── test_insert.py
   │  │  │     │     │        │  │  │  │  │  ├── test_repeat.py
   │  │  │     │     │        │  │  │  │  │  ├── test_shift.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_delete.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_freq_attr.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  │  ├── test_ops.py
   │  │  │     │     │        │  │  │  │  ├── test_pickle.py
   │  │  │     │     │        │  │  │  │  ├── test_scalar_compat.py
   │  │  │     │     │        │  │  │  │  ├── test_searchsorted.py
   │  │  │     │     │        │  │  │  │  ├── test_setops.py
   │  │  │     │     │        │  │  │  │  ├── test_timedelta.py
   │  │  │     │     │        │  │  │  │  ├── test_timedelta_range.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── indexing
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── interval
   │  │  │     │     │        │  │  │  │  ├── test_interval.py
   │  │  │     │     │        │  │  │  │  ├── test_interval_new.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── multiindex
   │  │  │     │     │        │  │  │  │  ├── test_chaining_and_caching.py
   │  │  │     │     │        │  │  │  │  ├── test_datetime.py
   │  │  │     │     │        │  │  │  │  ├── test_getitem.py
   │  │  │     │     │        │  │  │  │  ├── test_iloc.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing_slow.py
   │  │  │     │     │        │  │  │  │  ├── test_loc.py
   │  │  │     │     │        │  │  │  │  ├── test_multiindex.py
   │  │  │     │     │        │  │  │  │  ├── test_partial.py
   │  │  │     │     │        │  │  │  │  ├── test_setitem.py
   │  │  │     │     │        │  │  │  │  ├── test_slice.py
   │  │  │     │     │        │  │  │  │  ├── test_sorted.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_at.py
   │  │  │     │     │        │  │  │  ├── test_categorical.py
   │  │  │     │     │        │  │  │  ├── test_chaining_and_caching.py
   │  │  │     │     │        │  │  │  ├── test_check_indexer.py
   │  │  │     │     │        │  │  │  ├── test_coercion.py
   │  │  │     │     │        │  │  │  ├── test_datetime.py
   │  │  │     │     │        │  │  │  ├── test_floats.py
   │  │  │     │     │        │  │  │  ├── test_iat.py
   │  │  │     │     │        │  │  │  ├── test_iloc.py
   │  │  │     │     │        │  │  │  ├── test_indexers.py
   │  │  │     │     │        │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  ├── test_loc.py
   │  │  │     │     │        │  │  │  ├── test_na_indexing.py
   │  │  │     │     │        │  │  │  ├── test_partial.py
   │  │  │     │     │        │  │  │  ├── test_scalar.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── interchange
   │  │  │     │     │        │  │  │  ├── test_impl.py
   │  │  │     │     │        │  │  │  ├── test_spec_conformance.py
   │  │  │     │     │        │  │  │  ├── test_utils.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── internals
   │  │  │     │     │        │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  ├── test_internals.py
   │  │  │     │     │        │  │  │  ├── test_managers.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── io
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── excel
   │  │  │     │     │        │  │  │  │  ├── test_odf.py
   │  │  │     │     │        │  │  │  │  ├── test_odswriter.py
   │  │  │     │     │        │  │  │  │  ├── test_openpyxl.py
   │  │  │     │     │        │  │  │  │  ├── test_readers.py
   │  │  │     │     │        │  │  │  │  ├── test_style.py
   │  │  │     │     │        │  │  │  │  ├── test_writers.py
   │  │  │     │     │        │  │  │  │  ├── test_xlrd.py
   │  │  │     │     │        │  │  │  │  ├── test_xlsxwriter.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── formats
   │  │  │     │     │        │  │  │  │  ├── style
   │  │  │     │     │        │  │  │  │  │  ├── test_bar.py
   │  │  │     │     │        │  │  │  │  │  ├── test_exceptions.py
   │  │  │     │     │        │  │  │  │  │  ├── test_format.py
   │  │  │     │     │        │  │  │  │  │  ├── test_highlight.py
   │  │  │     │     │        │  │  │  │  │  ├── test_html.py
   │  │  │     │     │        │  │  │  │  │  ├── test_matplotlib.py
   │  │  │     │     │        │  │  │  │  │  ├── test_non_unique.py
   │  │  │     │     │        │  │  │  │  │  ├── test_style.py
   │  │  │     │     │        │  │  │  │  │  ├── test_tooltip.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_latex.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_string.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  ├── test_console.py
   │  │  │     │     │        │  │  │  │  ├── test_css.py
   │  │  │     │     │        │  │  │  │  ├── test_eng_formatting.py
   │  │  │     │     │        │  │  │  │  ├── test_format.py
   │  │  │     │     │        │  │  │  │  ├── test_ipython_compat.py
   │  │  │     │     │        │  │  │  │  ├── test_printing.py
   │  │  │     │     │        │  │  │  │  ├── test_to_csv.py
   │  │  │     │     │        │  │  │  │  ├── test_to_excel.py
   │  │  │     │     │        │  │  │  │  ├── test_to_html.py
   │  │  │     │     │        │  │  │  │  ├── test_to_latex.py
   │  │  │     │     │        │  │  │  │  ├── test_to_markdown.py
   │  │  │     │     │        │  │  │  │  ├── test_to_string.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── generate_legacy_storage_files.py
   │  │  │     │     │        │  │  │  ├── json
   │  │  │     │     │        │  │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  │  ├── test_compression.py
   │  │  │     │     │        │  │  │  │  ├── test_deprecated_kwargs.py
   │  │  │     │     │        │  │  │  │  ├── test_json_table_schema.py
   │  │  │     │     │        │  │  │  │  ├── test_json_table_schema_ext_dtype.py
   │  │  │     │     │        │  │  │  │  ├── test_normalize.py
   │  │  │     │     │        │  │  │  │  ├── test_pandas.py
   │  │  │     │     │        │  │  │  │  ├── test_readlines.py
   │  │  │     │     │        │  │  │  │  ├── test_ujson.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── parser
   │  │  │     │     │        │  │  │  │  ├── common
   │  │  │     │     │        │  │  │  │  │  ├── test_chunksize.py
   │  │  │     │     │        │  │  │  │  │  ├── test_common_basic.py
   │  │  │     │     │        │  │  │  │  │  ├── test_data_list.py
   │  │  │     │     │        │  │  │  │  │  ├── test_decimal.py
   │  │  │     │     │        │  │  │  │  │  ├── test_file_buffer_url.py
   │  │  │     │     │        │  │  │  │  │  ├── test_float.py
   │  │  │     │     │        │  │  │  │  │  ├── test_index.py
   │  │  │     │     │        │  │  │  │  │  ├── test_inf.py
   │  │  │     │     │        │  │  │  │  │  ├── test_ints.py
   │  │  │     │     │        │  │  │  │  │  ├── test_iterator.py
   │  │  │     │     │        │  │  │  │  │  ├── test_read_errors.py
   │  │  │     │     │        │  │  │  │  │  ├── test_verbose.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  │  ├── dtypes
   │  │  │     │     │        │  │  │  │  │  ├── test_categorical.py
   │  │  │     │     │        │  │  │  │  │  ├── test_dtypes_basic.py
   │  │  │     │     │        │  │  │  │  │  ├── test_empty.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  ├── test_comment.py
   │  │  │     │     │        │  │  │  │  ├── test_compression.py
   │  │  │     │     │        │  │  │  │  ├── test_concatenate_chunks.py
   │  │  │     │     │        │  │  │  │  ├── test_converters.py
   │  │  │     │     │        │  │  │  │  ├── test_c_parser_only.py
   │  │  │     │     │        │  │  │  │  ├── test_dialect.py
   │  │  │     │     │        │  │  │  │  ├── test_encoding.py
   │  │  │     │     │        │  │  │  │  ├── test_header.py
   │  │  │     │     │        │  │  │  │  ├── test_index_col.py
   │  │  │     │     │        │  │  │  │  ├── test_mangle_dupes.py
   │  │  │     │     │        │  │  │  │  ├── test_multi_thread.py
   │  │  │     │     │        │  │  │  │  ├── test_na_values.py
   │  │  │     │     │        │  │  │  │  ├── test_network.py
   │  │  │     │     │        │  │  │  │  ├── test_parse_dates.py
   │  │  │     │     │        │  │  │  │  ├── test_python_parser_only.py
   │  │  │     │     │        │  │  │  │  ├── test_quoting.py
   │  │  │     │     │        │  │  │  │  ├── test_read_fwf.py
   │  │  │     │     │        │  │  │  │  ├── test_skiprows.py
   │  │  │     │     │        │  │  │  │  ├── test_textreader.py
   │  │  │     │     │        │  │  │  │  ├── test_unsupported.py
   │  │  │     │     │        │  │  │  │  ├── test_upcast.py
   │  │  │     │     │        │  │  │  │  ├── usecols
   │  │  │     │     │        │  │  │  │  │  ├── test_parse_dates.py
   │  │  │     │     │        │  │  │  │  │  ├── test_strings.py
   │  │  │     │     │        │  │  │  │  │  ├── test_usecols_basic.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── pytables
   │  │  │     │     │        │  │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  │  ├── test_append.py
   │  │  │     │     │        │  │  │  │  ├── test_categorical.py
   │  │  │     │     │        │  │  │  │  ├── test_compat.py
   │  │  │     │     │        │  │  │  │  ├── test_complex.py
   │  │  │     │     │        │  │  │  │  ├── test_errors.py
   │  │  │     │     │        │  │  │  │  ├── test_file_handling.py
   │  │  │     │     │        │  │  │  │  ├── test_keys.py
   │  │  │     │     │        │  │  │  │  ├── test_put.py
   │  │  │     │     │        │  │  │  │  ├── test_pytables_missing.py
   │  │  │     │     │        │  │  │  │  ├── test_read.py
   │  │  │     │     │        │  │  │  │  ├── test_retain_attributes.py
   │  │  │     │     │        │  │  │  │  ├── test_round_trip.py
   │  │  │     │     │        │  │  │  │  ├── test_select.py
   │  │  │     │     │        │  │  │  │  ├── test_store.py
   │  │  │     │     │        │  │  │  │  ├── test_subclass.py
   │  │  │     │     │        │  │  │  │  ├── test_timezones.py
   │  │  │     │     │        │  │  │  │  ├── test_time_series.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── sas
   │  │  │     │     │        │  │  │  │  ├── test_byteswap.py
   │  │  │     │     │        │  │  │  │  ├── test_sas.py
   │  │  │     │     │        │  │  │  │  ├── test_sas7bdat.py
   │  │  │     │     │        │  │  │  │  ├── test_xport.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_clipboard.py
   │  │  │     │     │        │  │  │  ├── test_common.py
   │  │  │     │     │        │  │  │  ├── test_compression.py
   │  │  │     │     │        │  │  │  ├── test_feather.py
   │  │  │     │     │        │  │  │  ├── test_fsspec.py
   │  │  │     │     │        │  │  │  ├── test_gbq.py
   │  │  │     │     │        │  │  │  ├── test_gcs.py
   │  │  │     │     │        │  │  │  ├── test_html.py
   │  │  │     │     │        │  │  │  ├── test_http_headers.py
   │  │  │     │     │        │  │  │  ├── test_orc.py
   │  │  │     │     │        │  │  │  ├── test_parquet.py
   │  │  │     │     │        │  │  │  ├── test_pickle.py
   │  │  │     │     │        │  │  │  ├── test_s3.py
   │  │  │     │     │        │  │  │  ├── test_spss.py
   │  │  │     │     │        │  │  │  ├── test_sql.py
   │  │  │     │     │        │  │  │  ├── test_stata.py
   │  │  │     │     │        │  │  │  ├── xml
   │  │  │     │     │        │  │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  │  ├── test_to_xml.py
   │  │  │     │     │        │  │  │  │  ├── test_xml.py
   │  │  │     │     │        │  │  │  │  ├── test_xml_dtypes.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── libs
   │  │  │     │     │        │  │  │  ├── test_hashtable.py
   │  │  │     │     │        │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  ├── test_lib.py
   │  │  │     │     │        │  │  │  ├── test_libalgos.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── plotting
   │  │  │     │     │        │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── frame
   │  │  │     │     │        │  │  │  │  ├── test_frame.py
   │  │  │     │     │        │  │  │  │  ├── test_frame_color.py
   │  │  │     │     │        │  │  │  │  ├── test_frame_groupby.py
   │  │  │     │     │        │  │  │  │  ├── test_frame_legend.py
   │  │  │     │     │        │  │  │  │  ├── test_frame_subplots.py
   │  │  │     │     │        │  │  │  │  ├── test_hist_box_by.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_backend.py
   │  │  │     │     │        │  │  │  ├── test_boxplot_method.py
   │  │  │     │     │        │  │  │  ├── test_common.py
   │  │  │     │     │        │  │  │  ├── test_converter.py
   │  │  │     │     │        │  │  │  ├── test_datetimelike.py
   │  │  │     │     │        │  │  │  ├── test_groupby.py
   │  │  │     │     │        │  │  │  ├── test_hist_method.py
   │  │  │     │     │        │  │  │  ├── test_misc.py
   │  │  │     │     │        │  │  │  ├── test_series.py
   │  │  │     │     │        │  │  │  ├── test_style.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── reductions
   │  │  │     │     │        │  │  │  ├── test_reductions.py
   │  │  │     │     │        │  │  │  ├── test_stat_reductions.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── resample
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── test_base.py
   │  │  │     │     │        │  │  │  ├── test_datetime_index.py
   │  │  │     │     │        │  │  │  ├── test_period_index.py
   │  │  │     │     │        │  │  │  ├── test_resampler_grouper.py
   │  │  │     │     │        │  │  │  ├── test_resample_api.py
   │  │  │     │     │        │  │  │  ├── test_timedelta.py
   │  │  │     │     │        │  │  │  ├── test_time_grouper.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── reshape
   │  │  │     │     │        │  │  │  ├── concat
   │  │  │     │     │        │  │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  │  ├── test_append.py
   │  │  │     │     │        │  │  │  │  ├── test_append_common.py
   │  │  │     │     │        │  │  │  │  ├── test_categorical.py
   │  │  │     │     │        │  │  │  │  ├── test_concat.py
   │  │  │     │     │        │  │  │  │  ├── test_dataframe.py
   │  │  │     │     │        │  │  │  │  ├── test_datetimes.py
   │  │  │     │     │        │  │  │  │  ├── test_empty.py
   │  │  │     │     │        │  │  │  │  ├── test_index.py
   │  │  │     │     │        │  │  │  │  ├── test_invalid.py
   │  │  │     │     │        │  │  │  │  ├── test_series.py
   │  │  │     │     │        │  │  │  │  ├── test_sort.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── merge
   │  │  │     │     │        │  │  │  │  ├── test_join.py
   │  │  │     │     │        │  │  │  │  ├── test_merge.py
   │  │  │     │     │        │  │  │  │  ├── test_merge_asof.py
   │  │  │     │     │        │  │  │  │  ├── test_merge_cross.py
   │  │  │     │     │        │  │  │  │  ├── test_merge_index_as_string.py
   │  │  │     │     │        │  │  │  │  ├── test_merge_ordered.py
   │  │  │     │     │        │  │  │  │  ├── test_multi.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_crosstab.py
   │  │  │     │     │        │  │  │  ├── test_cut.py
   │  │  │     │     │        │  │  │  ├── test_from_dummies.py
   │  │  │     │     │        │  │  │  ├── test_get_dummies.py
   │  │  │     │     │        │  │  │  ├── test_melt.py
   │  │  │     │     │        │  │  │  ├── test_pivot.py
   │  │  │     │     │        │  │  │  ├── test_pivot_multilevel.py
   │  │  │     │     │        │  │  │  ├── test_qcut.py
   │  │  │     │     │        │  │  │  ├── test_union_categoricals.py
   │  │  │     │     │        │  │  │  ├── test_util.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── scalar
   │  │  │     │     │        │  │  │  ├── interval
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_contains.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_interval.py
   │  │  │     │     │        │  │  │  │  ├── test_overlaps.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── period
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_asfreq.py
   │  │  │     │     │        │  │  │  │  ├── test_period.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_nat.py
   │  │  │     │     │        │  │  │  ├── test_na_scalar.py
   │  │  │     │     │        │  │  │  ├── timedelta
   │  │  │     │     │        │  │  │  │  ├── methods
   │  │  │     │     │        │  │  │  │  │  ├── test_as_unit.py
   │  │  │     │     │        │  │  │  │  │  ├── test_round.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_timedelta.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── timestamp
   │  │  │     │     │        │  │  │  │  ├── methods
   │  │  │     │     │        │  │  │  │  │  ├── test_as_unit.py
   │  │  │     │     │        │  │  │  │  │  ├── test_normalize.py
   │  │  │     │     │        │  │  │  │  │  ├── test_replace.py
   │  │  │     │     │        │  │  │  │  │  ├── test_round.py
   │  │  │     │     │        │  │  │  │  │  ├── test_timestamp_method.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_julian_date.py
   │  │  │     │     │        │  │  │  │  │  ├── test_to_pydatetime.py
   │  │  │     │     │        │  │  │  │  │  ├── test_tz_convert.py
   │  │  │     │     │        │  │  │  │  │  ├── test_tz_localize.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  │  ├── test_comparisons.py
   │  │  │     │     │        │  │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  │  ├── test_timestamp.py
   │  │  │     │     │        │  │  │  │  ├── test_timezones.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── series
   │  │  │     │     │        │  │  │  ├── accessors
   │  │  │     │     │        │  │  │  │  ├── test_cat_accessor.py
   │  │  │     │     │        │  │  │  │  ├── test_dt_accessor.py
   │  │  │     │     │        │  │  │  │  ├── test_list_accessor.py
   │  │  │     │     │        │  │  │  │  ├── test_sparse_accessor.py
   │  │  │     │     │        │  │  │  │  ├── test_struct_accessor.py
   │  │  │     │     │        │  │  │  │  ├── test_str_accessor.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── indexing
   │  │  │     │     │        │  │  │  │  ├── test_datetime.py
   │  │  │     │     │        │  │  │  │  ├── test_delitem.py
   │  │  │     │     │        │  │  │  │  ├── test_get.py
   │  │  │     │     │        │  │  │  │  ├── test_getitem.py
   │  │  │     │     │        │  │  │  │  ├── test_indexing.py
   │  │  │     │     │        │  │  │  │  ├── test_mask.py
   │  │  │     │     │        │  │  │  │  ├── test_setitem.py
   │  │  │     │     │        │  │  │  │  ├── test_set_value.py
   │  │  │     │     │        │  │  │  │  ├── test_take.py
   │  │  │     │     │        │  │  │  │  ├── test_where.py
   │  │  │     │     │        │  │  │  │  ├── test_xs.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── methods
   │  │  │     │     │        │  │  │  │  ├── test_add_prefix_suffix.py
   │  │  │     │     │        │  │  │  │  ├── test_align.py
   │  │  │     │     │        │  │  │  │  ├── test_argsort.py
   │  │  │     │     │        │  │  │  │  ├── test_asof.py
   │  │  │     │     │        │  │  │  │  ├── test_astype.py
   │  │  │     │     │        │  │  │  │  ├── test_autocorr.py
   │  │  │     │     │        │  │  │  │  ├── test_between.py
   │  │  │     │     │        │  │  │  │  ├── test_case_when.py
   │  │  │     │     │        │  │  │  │  ├── test_clip.py
   │  │  │     │     │        │  │  │  │  ├── test_combine.py
   │  │  │     │     │        │  │  │  │  ├── test_combine_first.py
   │  │  │     │     │        │  │  │  │  ├── test_compare.py
   │  │  │     │     │        │  │  │  │  ├── test_convert_dtypes.py
   │  │  │     │     │        │  │  │  │  ├── test_copy.py
   │  │  │     │     │        │  │  │  │  ├── test_count.py
   │  │  │     │     │        │  │  │  │  ├── test_cov_corr.py
   │  │  │     │     │        │  │  │  │  ├── test_describe.py
   │  │  │     │     │        │  │  │  │  ├── test_diff.py
   │  │  │     │     │        │  │  │  │  ├── test_drop.py
   │  │  │     │     │        │  │  │  │  ├── test_dropna.py
   │  │  │     │     │        │  │  │  │  ├── test_drop_duplicates.py
   │  │  │     │     │        │  │  │  │  ├── test_dtypes.py
   │  │  │     │     │        │  │  │  │  ├── test_duplicated.py
   │  │  │     │     │        │  │  │  │  ├── test_equals.py
   │  │  │     │     │        │  │  │  │  ├── test_explode.py
   │  │  │     │     │        │  │  │  │  ├── test_fillna.py
   │  │  │     │     │        │  │  │  │  ├── test_get_numeric_data.py
   │  │  │     │     │        │  │  │  │  ├── test_head_tail.py
   │  │  │     │     │        │  │  │  │  ├── test_infer_objects.py
   │  │  │     │     │        │  │  │  │  ├── test_info.py
   │  │  │     │     │        │  │  │  │  ├── test_interpolate.py
   │  │  │     │     │        │  │  │  │  ├── test_isin.py
   │  │  │     │     │        │  │  │  │  ├── test_isna.py
   │  │  │     │     │        │  │  │  │  ├── test_is_monotonic.py
   │  │  │     │     │        │  │  │  │  ├── test_is_unique.py
   │  │  │     │     │        │  │  │  │  ├── test_item.py
   │  │  │     │     │        │  │  │  │  ├── test_map.py
   │  │  │     │     │        │  │  │  │  ├── test_matmul.py
   │  │  │     │     │        │  │  │  │  ├── test_nlargest.py
   │  │  │     │     │        │  │  │  │  ├── test_nunique.py
   │  │  │     │     │        │  │  │  │  ├── test_pct_change.py
   │  │  │     │     │        │  │  │  │  ├── test_pop.py
   │  │  │     │     │        │  │  │  │  ├── test_quantile.py
   │  │  │     │     │        │  │  │  │  ├── test_rank.py
   │  │  │     │     │        │  │  │  │  ├── test_reindex.py
   │  │  │     │     │        │  │  │  │  ├── test_reindex_like.py
   │  │  │     │     │        │  │  │  │  ├── test_rename.py
   │  │  │     │     │        │  │  │  │  ├── test_rename_axis.py
   │  │  │     │     │        │  │  │  │  ├── test_repeat.py
   │  │  │     │     │        │  │  │  │  ├── test_replace.py
   │  │  │     │     │        │  │  │  │  ├── test_reset_index.py
   │  │  │     │     │        │  │  │  │  ├── test_round.py
   │  │  │     │     │        │  │  │  │  ├── test_searchsorted.py
   │  │  │     │     │        │  │  │  │  ├── test_set_name.py
   │  │  │     │     │        │  │  │  │  ├── test_size.py
   │  │  │     │     │        │  │  │  │  ├── test_sort_index.py
   │  │  │     │     │        │  │  │  │  ├── test_sort_values.py
   │  │  │     │     │        │  │  │  │  ├── test_tolist.py
   │  │  │     │     │        │  │  │  │  ├── test_to_csv.py
   │  │  │     │     │        │  │  │  │  ├── test_to_dict.py
   │  │  │     │     │        │  │  │  │  ├── test_to_frame.py
   │  │  │     │     │        │  │  │  │  ├── test_to_numpy.py
   │  │  │     │     │        │  │  │  │  ├── test_truncate.py
   │  │  │     │     │        │  │  │  │  ├── test_tz_localize.py
   │  │  │     │     │        │  │  │  │  ├── test_unique.py
   │  │  │     │     │        │  │  │  │  ├── test_unstack.py
   │  │  │     │     │        │  │  │  │  ├── test_update.py
   │  │  │     │     │        │  │  │  │  ├── test_values.py
   │  │  │     │     │        │  │  │  │  ├── test_value_counts.py
   │  │  │     │     │        │  │  │  │  ├── test_view.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  ├── test_arithmetic.py
   │  │  │     │     │        │  │  │  ├── test_constructors.py
   │  │  │     │     │        │  │  │  ├── test_cumulative.py
   │  │  │     │     │        │  │  │  ├── test_formats.py
   │  │  │     │     │        │  │  │  ├── test_iteration.py
   │  │  │     │     │        │  │  │  ├── test_logical_ops.py
   │  │  │     │     │        │  │  │  ├── test_missing.py
   │  │  │     │     │        │  │  │  ├── test_npfuncs.py
   │  │  │     │     │        │  │  │  ├── test_reductions.py
   │  │  │     │     │        │  │  │  ├── test_subclass.py
   │  │  │     │     │        │  │  │  ├── test_ufunc.py
   │  │  │     │     │        │  │  │  ├── test_unary.py
   │  │  │     │     │        │  │  │  ├── test_validate.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── strings
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  ├── test_case_justify.py
   │  │  │     │     │        │  │  │  ├── test_cat.py
   │  │  │     │     │        │  │  │  ├── test_extract.py
   │  │  │     │     │        │  │  │  ├── test_find_replace.py
   │  │  │     │     │        │  │  │  ├── test_get_dummies.py
   │  │  │     │     │        │  │  │  ├── test_split_partition.py
   │  │  │     │     │        │  │  │  ├── test_strings.py
   │  │  │     │     │        │  │  │  ├── test_string_array.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── test_aggregation.py
   │  │  │     │     │        │  │  ├── test_algos.py
   │  │  │     │     │        │  │  ├── test_common.py
   │  │  │     │     │        │  │  ├── test_downstream.py
   │  │  │     │     │        │  │  ├── test_errors.py
   │  │  │     │     │        │  │  ├── test_expressions.py
   │  │  │     │     │        │  │  ├── test_flags.py
   │  │  │     │     │        │  │  ├── test_multilevel.py
   │  │  │     │     │        │  │  ├── test_nanops.py
   │  │  │     │     │        │  │  ├── test_optional_dependency.py
   │  │  │     │     │        │  │  ├── test_register_accessor.py
   │  │  │     │     │        │  │  ├── test_sorting.py
   │  │  │     │     │        │  │  ├── test_take.py
   │  │  │     │     │        │  │  ├── tools
   │  │  │     │     │        │  │  │  ├── test_to_datetime.py
   │  │  │     │     │        │  │  │  ├── test_to_numeric.py
   │  │  │     │     │        │  │  │  ├── test_to_time.py
   │  │  │     │     │        │  │  │  ├── test_to_timedelta.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── tseries
   │  │  │     │     │        │  │  │  ├── frequencies
   │  │  │     │     │        │  │  │  │  ├── test_frequencies.py
   │  │  │     │     │        │  │  │  │  ├── test_freq_code.py
   │  │  │     │     │        │  │  │  │  ├── test_inference.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── holiday
   │  │  │     │     │        │  │  │  │  ├── test_calendar.py
   │  │  │     │     │        │  │  │  │  ├── test_federal.py
   │  │  │     │     │        │  │  │  │  ├── test_holiday.py
   │  │  │     │     │        │  │  │  │  ├── test_observance.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── offsets
   │  │  │     │     │        │  │  │  │  ├── common.py
   │  │  │     │     │        │  │  │  │  ├── test_business_day.py
   │  │  │     │     │        │  │  │  │  ├── test_business_hour.py
   │  │  │     │     │        │  │  │  │  ├── test_business_month.py
   │  │  │     │     │        │  │  │  │  ├── test_business_quarter.py
   │  │  │     │     │        │  │  │  │  ├── test_business_year.py
   │  │  │     │     │        │  │  │  │  ├── test_common.py
   │  │  │     │     │        │  │  │  │  ├── test_custom_business_day.py
   │  │  │     │     │        │  │  │  │  ├── test_custom_business_hour.py
   │  │  │     │     │        │  │  │  │  ├── test_custom_business_month.py
   │  │  │     │     │        │  │  │  │  ├── test_dst.py
   │  │  │     │     │        │  │  │  │  ├── test_easter.py
   │  │  │     │     │        │  │  │  │  ├── test_fiscal.py
   │  │  │     │     │        │  │  │  │  ├── test_index.py
   │  │  │     │     │        │  │  │  │  ├── test_month.py
   │  │  │     │     │        │  │  │  │  ├── test_offsets.py
   │  │  │     │     │        │  │  │  │  ├── test_offsets_properties.py
   │  │  │     │     │        │  │  │  │  ├── test_quarter.py
   │  │  │     │     │        │  │  │  │  ├── test_ticks.py
   │  │  │     │     │        │  │  │  │  ├── test_week.py
   │  │  │     │     │        │  │  │  │  ├── test_year.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── tslibs
   │  │  │     │     │        │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  ├── test_array_to_datetime.py
   │  │  │     │     │        │  │  │  ├── test_ccalendar.py
   │  │  │     │     │        │  │  │  ├── test_conversion.py
   │  │  │     │     │        │  │  │  ├── test_fields.py
   │  │  │     │     │        │  │  │  ├── test_libfrequencies.py
   │  │  │     │     │        │  │  │  ├── test_liboffsets.py
   │  │  │     │     │        │  │  │  ├── test_npy_units.py
   │  │  │     │     │        │  │  │  ├── test_np_datetime.py
   │  │  │     │     │        │  │  │  ├── test_parse_iso8601.py
   │  │  │     │     │        │  │  │  ├── test_parsing.py
   │  │  │     │     │        │  │  │  ├── test_period.py
   │  │  │     │     │        │  │  │  ├── test_resolution.py
   │  │  │     │     │        │  │  │  ├── test_strptime.py
   │  │  │     │     │        │  │  │  ├── test_timedeltas.py
   │  │  │     │     │        │  │  │  ├── test_timezones.py
   │  │  │     │     │        │  │  │  ├── test_to_offset.py
   │  │  │     │     │        │  │  │  ├── test_tzconversion.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── util
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── test_assert_almost_equal.py
   │  │  │     │     │        │  │  │  ├── test_assert_attr_equal.py
   │  │  │     │     │        │  │  │  ├── test_assert_categorical_equal.py
   │  │  │     │     │        │  │  │  ├── test_assert_extension_array_equal.py
   │  │  │     │     │        │  │  │  ├── test_assert_frame_equal.py
   │  │  │     │     │        │  │  │  ├── test_assert_index_equal.py
   │  │  │     │     │        │  │  │  ├── test_assert_interval_array_equal.py
   │  │  │     │     │        │  │  │  ├── test_assert_numpy_array_equal.py
   │  │  │     │     │        │  │  │  ├── test_assert_produces_warning.py
   │  │  │     │     │        │  │  │  ├── test_assert_series_equal.py
   │  │  │     │     │        │  │  │  ├── test_deprecate.py
   │  │  │     │     │        │  │  │  ├── test_deprecate_kwarg.py
   │  │  │     │     │        │  │  │  ├── test_deprecate_nonkeyword_arguments.py
   │  │  │     │     │        │  │  │  ├── test_doc.py
   │  │  │     │     │        │  │  │  ├── test_hashing.py
   │  │  │     │     │        │  │  │  ├── test_numba.py
   │  │  │     │     │        │  │  │  ├── test_rewrite_warning.py
   │  │  │     │     │        │  │  │  ├── test_shares_memory.py
   │  │  │     │     │        │  │  │  ├── test_show_versions.py
   │  │  │     │     │        │  │  │  ├── test_util.py
   │  │  │     │     │        │  │  │  ├── test_validate_args.py
   │  │  │     │     │        │  │  │  ├── test_validate_args_and_kwargs.py
   │  │  │     │     │        │  │  │  ├── test_validate_inclusive.py
   │  │  │     │     │        │  │  │  ├── test_validate_kwargs.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── window
   │  │  │     │     │        │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  ├── moments
   │  │  │     │     │        │  │  │  │  ├── conftest.py
   │  │  │     │     │        │  │  │  │  ├── test_moments_consistency_ewm.py
   │  │  │     │     │        │  │  │  │  ├── test_moments_consistency_expanding.py
   │  │  │     │     │        │  │  │  │  ├── test_moments_consistency_rolling.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── test_api.py
   │  │  │     │     │        │  │  │  ├── test_apply.py
   │  │  │     │     │        │  │  │  ├── test_base_indexer.py
   │  │  │     │     │        │  │  │  ├── test_cython_aggregations.py
   │  │  │     │     │        │  │  │  ├── test_dtypes.py
   │  │  │     │     │        │  │  │  ├── test_ewm.py
   │  │  │     │     │        │  │  │  ├── test_expanding.py
   │  │  │     │     │        │  │  │  ├── test_groupby.py
   │  │  │     │     │        │  │  │  ├── test_numba.py
   │  │  │     │     │        │  │  │  ├── test_online.py
   │  │  │     │     │        │  │  │  ├── test_pairwise.py
   │  │  │     │     │        │  │  │  ├── test_rolling.py
   │  │  │     │     │        │  │  │  ├── test_rolling_functions.py
   │  │  │     │     │        │  │  │  ├── test_rolling_quantile.py
   │  │  │     │     │        │  │  │  ├── test_rolling_skew_kurt.py
   │  │  │     │     │        │  │  │  ├── test_timeseries_window.py
   │  │  │     │     │        │  │  │  ├── test_win_type.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── tseries
   │  │  │     │     │        │  │  ├── api.py
   │  │  │     │     │        │  │  ├── frequencies.py
   │  │  │     │     │        │  │  ├── holiday.py
   │  │  │     │     │        │  │  ├── offsets.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── util
   │  │  │     │     │        │  │  ├── version
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── _decorators.py
   │  │  │     │     │        │  │  ├── _doctools.py
   │  │  │     │     │        │  │  ├── _exceptions.py
   │  │  │     │     │        │  │  ├── _print_versions.py
   │  │  │     │     │        │  │  ├── _tester.py
   │  │  │     │     │        │  │  ├── _test_decorators.py
   │  │  │     │     │        │  │  ├── _validators.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── _config
   │  │  │     │     │        │  │  ├── config.py
   │  │  │     │     │        │  │  ├── dates.py
   │  │  │     │     │        │  │  ├── display.py
   │  │  │     │     │        │  │  ├── localization.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── _libs
   │  │  │     │     │        │  │  ├── algos.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── algos.pyi
   │  │  │     │     │        │  │  ├── arrays.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── arrays.pyi
   │  │  │     │     │        │  │  ├── byteswap.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── byteswap.pyi
   │  │  │     │     │        │  │  ├── groupby.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── groupby.pyi
   │  │  │     │     │        │  │  ├── hashing.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── hashing.pyi
   │  │  │     │     │        │  │  ├── hashtable.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── hashtable.pyi
   │  │  │     │     │        │  │  ├── index.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── index.pyi
   │  │  │     │     │        │  │  ├── indexing.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── indexing.pyi
   │  │  │     │     │        │  │  ├── internals.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── internals.pyi
   │  │  │     │     │        │  │  ├── interval.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── interval.pyi
   │  │  │     │     │        │  │  ├── join.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── join.pyi
   │  │  │     │     │        │  │  ├── json.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── json.pyi
   │  │  │     │     │        │  │  ├── lib.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── lib.pyi
   │  │  │     │     │        │  │  ├── missing.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── missing.pyi
   │  │  │     │     │        │  │  ├── ops.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── ops.pyi
   │  │  │     │     │        │  │  ├── ops_dispatch.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── ops_dispatch.pyi
   │  │  │     │     │        │  │  ├── pandas_datetime.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── pandas_parser.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── parsers.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── parsers.pyi
   │  │  │     │     │        │  │  ├── properties.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── properties.pyi
   │  │  │     │     │        │  │  ├── reshape.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── reshape.pyi
   │  │  │     │     │        │  │  ├── sas.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── sas.pyi
   │  │  │     │     │        │  │  ├── sparse.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── sparse.pyi
   │  │  │     │     │        │  │  ├── testing.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── testing.pyi
   │  │  │     │     │        │  │  ├── tslib.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── tslib.pyi
   │  │  │     │     │        │  │  ├── tslibs
   │  │  │     │     │        │  │  │  ├── base.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── ccalendar.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── ccalendar.pyi
   │  │  │     │     │        │  │  │  ├── conversion.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── conversion.pyi
   │  │  │     │     │        │  │  │  ├── dtypes.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── dtypes.pyi
   │  │  │     │     │        │  │  │  ├── fields.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── fields.pyi
   │  │  │     │     │        │  │  │  ├── nattype.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── nattype.pyi
   │  │  │     │     │        │  │  │  ├── np_datetime.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── np_datetime.pyi
   │  │  │     │     │        │  │  │  ├── offsets.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── offsets.pyi
   │  │  │     │     │        │  │  │  ├── parsing.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── parsing.pyi
   │  │  │     │     │        │  │  │  ├── period.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── period.pyi
   │  │  │     │     │        │  │  │  ├── strptime.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── strptime.pyi
   │  │  │     │     │        │  │  │  ├── timedeltas.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── timedeltas.pyi
   │  │  │     │     │        │  │  │  ├── timestamps.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── timestamps.pyi
   │  │  │     │     │        │  │  │  ├── timezones.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── timezones.pyi
   │  │  │     │     │        │  │  │  ├── tzconversion.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── tzconversion.pyi
   │  │  │     │     │        │  │  │  ├── vectorized.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── vectorized.pyi
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── window
   │  │  │     │     │        │  │  │  ├── aggregations.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── aggregations.pyi
   │  │  │     │     │        │  │  │  ├── indexers.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  │  ├── indexers.pyi
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── writers.cpython-313-x86_64-linux-gnu.so
   │  │  │     │     │        │  │  ├── writers.pyi
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── _testing
   │  │  │     │     │        │  │  ├── asserters.py
   │  │  │     │     │        │  │  ├── compat.py
   │  │  │     │     │        │  │  ├── contexts.py
   │  │  │     │     │        │  │  ├── _hypothesis.py
   │  │  │     │     │        │  │  ├── _io.py
   │  │  │     │     │        │  │  ├── _warnings.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── _typing.py
   │  │  │     │     │        │  ├── _version.py
   │  │  │     │     │        │  ├── _version_meson.py
   │  │  │     │     │        │  └── __init__.py
   │  │  │     │     │       ├── pandas-2.3.3.dist-info
   │  │  │     │     │        │  ├── entry_points.txt
   │  │  │     │     │        │  ├── INSTALLER
   │  │  │     │     │        │  ├── LICENSE
   │  │  │     │     │        │  ├── METADATA
   │  │  │     │     │        │  ├── RECORD
   │  │  │     │     │        │  ├── REQUESTED
   │  │  │     │     │        │  └── WHEEL
   │  │  │     │     │       ├── pip
   │  │  │     │     │        │  ├── py.typed
   │  │  │     │     │        │  ├── _internal
   │  │  │     │     │        │  │  ├── build_env.py
   │  │  │     │     │        │  │  ├── cache.py
   │  │  │     │     │        │  │  ├── cli
   │  │  │     │     │        │  │  │  ├── autocompletion.py
   │  │  │     │     │        │  │  │  ├── base_command.py
   │  │  │     │     │        │  │  │  ├── cmdoptions.py
   │  │  │     │     │        │  │  │  ├── command_context.py
   │  │  │     │     │        │  │  │  ├── index_command.py
   │  │  │     │     │        │  │  │  ├── main.py
   │  │  │     │     │        │  │  │  ├── main_parser.py
   │  │  │     │     │        │  │  │  ├── parser.py
   │  │  │     │     │        │  │  │  ├── progress_bars.py
   │  │  │     │     │        │  │  │  ├── req_command.py
   │  │  │     │     │        │  │  │  ├── spinners.py
   │  │  │     │     │        │  │  │  ├── status_codes.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── commands
   │  │  │     │     │        │  │  │  ├── cache.py
   │  │  │     │     │        │  │  │  ├── check.py
   │  │  │     │     │        │  │  │  ├── completion.py
   │  │  │     │     │        │  │  │  ├── configuration.py
   │  │  │     │     │        │  │  │  ├── debug.py
   │  │  │     │     │        │  │  │  ├── download.py
   │  │  │     │     │        │  │  │  ├── freeze.py
   │  │  │     │     │        │  │  │  ├── hash.py
   │  │  │     │     │        │  │  │  ├── help.py
   │  │  │     │     │        │  │  │  ├── index.py
   │  │  │     │     │        │  │  │  ├── inspect.py
   │  │  │     │     │        │  │  │  ├── install.py
   │  │  │     │     │        │  │  │  ├── list.py
   │  │  │     │     │        │  │  │  ├── lock.py
   │  │  │     │     │        │  │  │  ├── search.py
   │  │  │     │     │        │  │  │  ├── show.py
   │  │  │     │     │        │  │  │  ├── uninstall.py
   │  │  │     │     │        │  │  │  ├── wheel.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── configuration.py
   │  │  │     │     │        │  │  ├── distributions
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── installed.py
   │  │  │     │     │        │  │  │  ├── sdist.py
   │  │  │     │     │        │  │  │  ├── wheel.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── exceptions.py
   │  │  │     │     │        │  │  ├── index
   │  │  │     │     │        │  │  │  ├── collector.py
   │  │  │     │     │        │  │  │  ├── package_finder.py
   │  │  │     │     │        │  │  │  ├── sources.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── locations
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── _distutils.py
   │  │  │     │     │        │  │  │  ├── _sysconfig.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── main.py
   │  │  │     │     │        │  │  ├── metadata
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── importlib
   │  │  │     │     │        │  │  │  │  ├── _compat.py
   │  │  │     │     │        │  │  │  │  ├── _dists.py
   │  │  │     │     │        │  │  │  │  ├── _envs.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── pkg_resources.py
   │  │  │     │     │        │  │  │  ├── _json.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── models
   │  │  │     │     │        │  │  │  ├── candidate.py
   │  │  │     │     │        │  │  │  ├── direct_url.py
   │  │  │     │     │        │  │  │  ├── format_control.py
   │  │  │     │     │        │  │  │  ├── index.py
   │  │  │     │     │        │  │  │  ├── installation_report.py
   │  │  │     │     │        │  │  │  ├── link.py
   │  │  │     │     │        │  │  │  ├── pylock.py
   │  │  │     │     │        │  │  │  ├── scheme.py
   │  │  │     │     │        │  │  │  ├── search_scope.py
   │  │  │     │     │        │  │  │  ├── selection_prefs.py
   │  │  │     │     │        │  │  │  ├── target_python.py
   │  │  │     │     │        │  │  │  ├── wheel.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── network
   │  │  │     │     │        │  │  │  ├── auth.py
   │  │  │     │     │        │  │  │  ├── cache.py
   │  │  │     │     │        │  │  │  ├── download.py
   │  │  │     │     │        │  │  │  ├── lazy_wheel.py
   │  │  │     │     │        │  │  │  ├── session.py
   │  │  │     │     │        │  │  │  ├── utils.py
   │  │  │     │     │        │  │  │  ├── xmlrpc.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── operations
   │  │  │     │     │        │  │  │  ├── build
   │  │  │     │     │        │  │  │  │  ├── build_tracker.py
   │  │  │     │     │        │  │  │  │  ├── metadata.py
   │  │  │     │     │        │  │  │  │  ├── metadata_editable.py
   │  │  │     │     │        │  │  │  │  ├── metadata_legacy.py
   │  │  │     │     │        │  │  │  │  ├── wheel.py
   │  │  │     │     │        │  │  │  │  ├── wheel_editable.py
   │  │  │     │     │        │  │  │  │  ├── wheel_legacy.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── check.py
   │  │  │     │     │        │  │  │  ├── freeze.py
   │  │  │     │     │        │  │  │  ├── install
   │  │  │     │     │        │  │  │  │  ├── editable_legacy.py
   │  │  │     │     │        │  │  │  │  ├── wheel.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── prepare.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── pyproject.py
   │  │  │     │     │        │  │  ├── req
   │  │  │     │     │        │  │  │  ├── constructors.py
   │  │  │     │     │        │  │  │  ├── req_dependency_group.py
   │  │  │     │     │        │  │  │  ├── req_file.py
   │  │  │     │     │        │  │  │  ├── req_install.py
   │  │  │     │     │        │  │  │  ├── req_set.py
   │  │  │     │     │        │  │  │  ├── req_uninstall.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── resolution
   │  │  │     │     │        │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  ├── legacy
   │  │  │     │     │        │  │  │  │  ├── resolver.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── resolvelib
   │  │  │     │     │        │  │  │  │  ├── base.py
   │  │  │     │     │        │  │  │  │  ├── candidates.py
   │  │  │     │     │        │  │  │  │  ├── factory.py
   │  │  │     │     │        │  │  │  │  ├── found_candidates.py
   │  │  │     │     │        │  │  │  │  ├── provider.py
   │  │  │     │     │        │  │  │  │  ├── reporter.py
   │  │  │     │     │        │  │  │  │  ├── requirements.py
   │  │  │     │     │        │  │  │  │  ├── resolver.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── self_outdated_check.py
   │  │  │     │     │        │  │  ├── utils
   │  │  │     │     │        │  │  │  ├── appdirs.py
   │  │  │     │     │        │  │  │  ├── compat.py
   │  │  │     │     │        │  │  │  ├── compatibility_tags.py
   │  │  │     │     │        │  │  │  ├── datetime.py
   │  │  │     │     │        │  │  │  ├── deprecation.py
   │  │  │     │     │        │  │  │  ├── direct_url_helpers.py
   │  │  │     │     │        │  │  │  ├── egg_link.py
   │  │  │     │     │        │  │  │  ├── entrypoints.py
   │  │  │     │     │        │  │  │  ├── filesystem.py
   │  │  │     │     │        │  │  │  ├── filetypes.py
   │  │  │     │     │        │  │  │  ├── glibc.py
   │  │  │     │     │        │  │  │  ├── hashes.py
   │  │  │     │     │        │  │  │  ├── logging.py
   │  │  │     │     │        │  │  │  ├── misc.py
   │  │  │     │     │        │  │  │  ├── packaging.py
   │  │  │     │     │        │  │  │  ├── retry.py
   │  │  │     │     │        │  │  │  ├── setuptools_build.py
   │  │  │     │     │        │  │  │  ├── subprocess.py
   │  │  │     │     │        │  │  │  ├── temp_dir.py
   │  │  │     │     │        │  │  │  ├── unpacking.py
   │  │  │     │     │        │  │  │  ├── urls.py
   │  │  │     │     │        │  │  │  ├── virtualenv.py
   │  │  │     │     │        │  │  │  ├── wheel.py
   │  │  │     │     │        │  │  │  ├── _jaraco_text.py
   │  │  │     │     │        │  │  │  ├── _log.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── vcs
   │  │  │     │     │        │  │  │  ├── bazaar.py
   │  │  │     │     │        │  │  │  ├── git.py
   │  │  │     │     │        │  │  │  ├── mercurial.py
   │  │  │     │     │        │  │  │  ├── subversion.py
   │  │  │     │     │        │  │  │  ├── versioncontrol.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── wheel_builder.py
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── _vendor
   │  │  │     │     │        │  │  ├── cachecontrol
   │  │  │     │     │        │  │  │  ├── adapter.py
   │  │  │     │     │        │  │  │  ├── cache.py
   │  │  │     │     │        │  │  │  ├── caches
   │  │  │     │     │        │  │  │  │  ├── file_cache.py
   │  │  │     │     │        │  │  │  │  ├── redis_cache.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── controller.py
   │  │  │     │     │        │  │  │  ├── filewrapper.py
   │  │  │     │     │        │  │  │  ├── heuristics.py
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── serialize.py
   │  │  │     │     │        │  │  │  ├── wrapper.py
   │  │  │     │     │        │  │  │  ├── _cmd.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── certifi
   │  │  │     │     │        │  │  │  ├── cacert.pem
   │  │  │     │     │        │  │  │  ├── core.py
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── __init__.py
   │  │  │     │     │        │  │  │  └── __main__.py
   │  │  │     │     │        │  │  ├── dependency_groups
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── _implementation.py
   │  │  │     │     │        │  │  │  ├── _lint_dependency_groups.py
   │  │  │     │     │        │  │  │  ├── _pip_wrapper.py
   │  │  │     │     │        │  │  │  ├── _toml_compat.py
   │  │  │     │     │        │  │  │  ├── __init__.py
   │  │  │     │     │        │  │  │  └── __main__.py
   │  │  │     │     │        │  │  ├── distlib
   │  │  │     │     │        │  │  │  ├── compat.py
   │  │  │     │     │        │  │  │  ├── resources.py
   │  │  │     │     │        │  │  │  ├── scripts.py
   │  │  │     │     │        │  │  │  ├── t32.exe
   │  │  │     │     │        │  │  │  ├── t64-arm.exe
   │  │  │     │     │        │  │  │  ├── t64.exe
   │  │  │     │     │        │  │  │  ├── util.py
   │  │  │     │     │        │  │  │  ├── w32.exe
   │  │  │     │     │        │  │  │  ├── w64-arm.exe
   │  │  │     │     │        │  │  │  ├── w64.exe
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── distro
   │  │  │     │     │        │  │  │  ├── distro.py
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── __init__.py
   │  │  │     │     │        │  │  │  └── __main__.py
   │  │  │     │     │        │  │  ├── idna
   │  │  │     │     │        │  │  │  ├── codec.py
   │  │  │     │     │        │  │  │  ├── compat.py
   │  │  │     │     │        │  │  │  ├── core.py
   │  │  │     │     │        │  │  │  ├── idnadata.py
   │  │  │     │     │        │  │  │  ├── intranges.py
   │  │  │     │     │        │  │  │  ├── package_data.py
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── uts46data.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── msgpack
   │  │  │     │     │        │  │  │  ├── exceptions.py
   │  │  │     │     │        │  │  │  ├── ext.py
   │  │  │     │     │        │  │  │  ├── fallback.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── packaging
   │  │  │     │     │        │  │  │  ├── licenses
   │  │  │     │     │        │  │  │  │  ├── _spdx.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── markers.py
   │  │  │     │     │        │  │  │  ├── metadata.py
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── requirements.py
   │  │  │     │     │        │  │  │  ├── specifiers.py
   │  │  │     │     │        │  │  │  ├── tags.py
   │  │  │     │     │        │  │  │  ├── utils.py
   │  │  │     │     │        │  │  │  ├── version.py
   │  │  │     │     │        │  │  │  ├── _elffile.py
   │  │  │     │     │        │  │  │  ├── _manylinux.py
   │  │  │     │     │        │  │  │  ├── _musllinux.py
   │  │  │     │     │        │  │  │  ├── _parser.py
   │  │  │     │     │        │  │  │  ├── _structures.py
   │  │  │     │     │        │  │  │  ├── _tokenizer.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── pkg_resources
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── platformdirs
   │  │  │     │     │        │  │  │  ├── android.py
   │  │  │     │     │        │  │  │  ├── api.py
   │  │  │     │     │        │  │  │  ├── macos.py
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── unix.py
   │  │  │     │     │        │  │  │  ├── version.py
   │  │  │     │     │        │  │  │  ├── windows.py
   │  │  │     │     │        │  │  │  ├── __init__.py
   │  │  │     │     │        │  │  │  └── __main__.py
   │  │  │     │     │        │  │  ├── pygments
   │  │  │     │     │        │  │  │  ├── console.py
   │  │  │     │     │        │  │  │  ├── filter.py
   │  │  │     │     │        │  │  │  ├── filters
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── formatter.py
   │  │  │     │     │        │  │  │  ├── formatters
   │  │  │     │     │        │  │  │  │  ├── _mapping.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── lexer.py
   │  │  │     │     │        │  │  │  ├── lexers
   │  │  │     │     │        │  │  │  │  ├── python.py
   │  │  │     │     │        │  │  │  │  ├── _mapping.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── modeline.py
   │  │  │     │     │        │  │  │  ├── plugin.py
   │  │  │     │     │        │  │  │  ├── regexopt.py
   │  │  │     │     │        │  │  │  ├── scanner.py
   │  │  │     │     │        │  │  │  ├── sphinxext.py
   │  │  │     │     │        │  │  │  ├── style.py
   │  │  │     │     │        │  │  │  ├── styles
   │  │  │     │     │        │  │  │  │  ├── _mapping.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── token.py
   │  │  │     │     │        │  │  │  ├── unistring.py
   │  │  │     │     │        │  │  │  ├── util.py
   │  │  │     │     │        │  │  │  ├── __init__.py
   │  │  │     │     │        │  │  │  └── __main__.py
   │  │  │     │     │        │  │  ├── pyproject_hooks
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── _impl.py
   │  │  │     │     │        │  │  │  ├── _in_process
   │  │  │     │     │        │  │  │  │  ├── _in_process.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── requests
   │  │  │     │     │        │  │  │  ├── adapters.py
   │  │  │     │     │        │  │  │  ├── api.py
   │  │  │     │     │        │  │  │  ├── auth.py
   │  │  │     │     │        │  │  │  ├── certs.py
   │  │  │     │     │        │  │  │  ├── compat.py
   │  │  │     │     │        │  │  │  ├── cookies.py
   │  │  │     │     │        │  │  │  ├── exceptions.py
   │  │  │     │     │        │  │  │  ├── help.py
   │  │  │     │     │        │  │  │  ├── hooks.py
   │  │  │     │     │        │  │  │  ├── models.py
   │  │  │     │     │        │  │  │  ├── packages.py
   │  │  │     │     │        │  │  │  ├── sessions.py
   │  │  │     │     │        │  │  │  ├── status_codes.py
   │  │  │     │     │        │  │  │  ├── structures.py
   │  │  │     │     │        │  │  │  ├── utils.py
   │  │  │     │     │        │  │  │  ├── _internal_utils.py
   │  │  │     │     │        │  │  │  ├── __init__.py
   │  │  │     │     │        │  │  │  └── __version__.py
   │  │  │     │     │        │  │  ├── resolvelib
   │  │  │     │     │        │  │  │  ├── providers.py
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── reporters.py
   │  │  │     │     │        │  │  │  ├── resolvers
   │  │  │     │     │        │  │  │  │  ├── abstract.py
   │  │  │     │     │        │  │  │  │  ├── criterion.py
   │  │  │     │     │        │  │  │  │  ├── exceptions.py
   │  │  │     │     │        │  │  │  │  ├── resolution.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── structs.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── rich
   │  │  │     │     │        │  │  │  ├── abc.py
   │  │  │     │     │        │  │  │  ├── align.py
   │  │  │     │     │        │  │  │  ├── ansi.py
   │  │  │     │     │        │  │  │  ├── bar.py
   │  │  │     │     │        │  │  │  ├── box.py
   │  │  │     │     │        │  │  │  ├── cells.py
   │  │  │     │     │        │  │  │  ├── color.py
   │  │  │     │     │        │  │  │  ├── color_triplet.py
   │  │  │     │     │        │  │  │  ├── columns.py
   │  │  │     │     │        │  │  │  ├── console.py
   │  │  │     │     │        │  │  │  ├── constrain.py
   │  │  │     │     │        │  │  │  ├── containers.py
   │  │  │     │     │        │  │  │  ├── control.py
   │  │  │     │     │        │  │  │  ├── default_styles.py
   │  │  │     │     │        │  │  │  ├── diagnose.py
   │  │  │     │     │        │  │  │  ├── emoji.py
   │  │  │     │     │        │  │  │  ├── errors.py
   │  │  │     │     │        │  │  │  ├── filesize.py
   │  │  │     │     │        │  │  │  ├── file_proxy.py
   │  │  │     │     │        │  │  │  ├── highlighter.py
   │  │  │     │     │        │  │  │  ├── json.py
   │  │  │     │     │        │  │  │  ├── jupyter.py
   │  │  │     │     │        │  │  │  ├── layout.py
   │  │  │     │     │        │  │  │  ├── live.py
   │  │  │     │     │        │  │  │  ├── live_render.py
   │  │  │     │     │        │  │  │  ├── logging.py
   │  │  │     │     │        │  │  │  ├── markup.py
   │  │  │     │     │        │  │  │  ├── measure.py
   │  │  │     │     │        │  │  │  ├── padding.py
   │  │  │     │     │        │  │  │  ├── pager.py
   │  │  │     │     │        │  │  │  ├── palette.py
   │  │  │     │     │        │  │  │  ├── panel.py
   │  │  │     │     │        │  │  │  ├── pretty.py
   │  │  │     │     │        │  │  │  ├── progress.py
   │  │  │     │     │        │  │  │  ├── progress_bar.py
   │  │  │     │     │        │  │  │  ├── prompt.py
   │  │  │     │     │        │  │  │  ├── protocol.py
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── region.py
   │  │  │     │     │        │  │  │  ├── repr.py
   │  │  │     │     │        │  │  │  ├── rule.py
   │  │  │     │     │        │  │  │  ├── scope.py
   │  │  │     │     │        │  │  │  ├── screen.py
   │  │  │     │     │        │  │  │  ├── segment.py
   │  │  │     │     │        │  │  │  ├── spinner.py
   │  │  │     │     │        │  │  │  ├── status.py
   │  │  │     │     │        │  │  │  ├── style.py
   │  │  │     │     │        │  │  │  ├── styled.py
   │  │  │     │     │        │  │  │  ├── syntax.py
   │  │  │     │     │        │  │  │  ├── table.py
   │  │  │     │     │        │  │  │  ├── terminal_theme.py
   │  │  │     │     │        │  │  │  ├── text.py
   │  │  │     │     │        │  │  │  ├── theme.py
   │  │  │     │     │        │  │  │  ├── themes.py
   │  │  │     │     │        │  │  │  ├── traceback.py
   │  │  │     │     │        │  │  │  ├── tree.py
   │  │  │     │     │        │  │  │  ├── _cell_widths.py
   │  │  │     │     │        │  │  │  ├── _emoji_codes.py
   │  │  │     │     │        │  │  │  ├── _emoji_replace.py
   │  │  │     │     │        │  │  │  ├── _export_format.py
   │  │  │     │     │        │  │  │  ├── _extension.py
   │  │  │     │     │        │  │  │  ├── _fileno.py
   │  │  │     │     │        │  │  │  ├── _inspect.py
   │  │  │     │     │        │  │  │  ├── _log_render.py
   │  │  │     │     │        │  │  │  ├── _loop.py
   │  │  │     │     │        │  │  │  ├── _null_file.py
   │  │  │     │     │        │  │  │  ├── _palettes.py
   │  │  │     │     │        │  │  │  ├── _pick.py
   │  │  │     │     │        │  │  │  ├── _ratio.py
   │  │  │     │     │        │  │  │  ├── _spinners.py
   │  │  │     │     │        │  │  │  ├── _stack.py
   │  │  │     │     │        │  │  │  ├── _timer.py
   │  │  │     │     │        │  │  │  ├── _win32_console.py
   │  │  │     │     │        │  │  │  ├── _windows.py
   │  │  │     │     │        │  │  │  ├── _windows_renderer.py
   │  │  │     │     │        │  │  │  ├── _wrap.py
   │  │  │     │     │        │  │  │  ├── __init__.py
   │  │  │     │     │        │  │  │  └── __main__.py
   │  │  │     │     │        │  │  ├── tomli
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── _parser.py
   │  │  │     │     │        │  │  │  ├── _re.py
   │  │  │     │     │        │  │  │  ├── _types.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── tomli_w
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── _writer.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── truststore
   │  │  │     │     │        │  │  │  ├── py.typed
   │  │  │     │     │        │  │  │  ├── _api.py
   │  │  │     │     │        │  │  │  ├── _macos.py
   │  │  │     │     │        │  │  │  ├── _openssl.py
   │  │  │     │     │        │  │  │  ├── _ssl_constants.py
   │  │  │     │     │        │  │  │  ├── _windows.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── urllib3
   │  │  │     │     │        │  │  │  ├── connection.py
   │  │  │     │     │        │  │  │  ├── connectionpool.py
   │  │  │     │     │        │  │  │  ├── contrib
   │  │  │     │     │        │  │  │  │  ├── appengine.py
   │  │  │     │     │        │  │  │  │  ├── ntlmpool.py
   │  │  │     │     │        │  │  │  │  ├── pyopenssl.py
   │  │  │     │     │        │  │  │  │  ├── securetransport.py
   │  │  │     │     │        │  │  │  │  ├── socks.py
   │  │  │     │     │        │  │  │  │  ├── _appengine_environ.py
   │  │  │     │     │        │  │  │  │  ├── _securetransport
   │  │  │     │     │        │  │  │  │  │  ├── bindings.py
   │  │  │     │     │        │  │  │  │  │  ├── low_level.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── exceptions.py
   │  │  │     │     │        │  │  │  ├── fields.py
   │  │  │     │     │        │  │  │  ├── filepost.py
   │  │  │     │     │        │  │  │  ├── packages
   │  │  │     │     │        │  │  │  │  ├── backports
   │  │  │     │     │        │  │  │  │  │  ├── makefile.py
   │  │  │     │     │        │  │  │  │  │  ├── weakref_finalize.py
   │  │  │     │     │        │  │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  │  ├── six.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── poolmanager.py
   │  │  │     │     │        │  │  │  ├── request.py
   │  │  │     │     │        │  │  │  ├── response.py
   │  │  │     │     │        │  │  │  ├── util
   │  │  │     │     │        │  │  │  │  ├── connection.py
   │  │  │     │     │        │  │  │  │  ├── proxy.py
   │  │  │     │     │        │  │  │  │  ├── queue.py
   │  │  │     │     │        │  │  │  │  ├── request.py
   │  │  │     │     │        │  │  │  │  ├── response.py
   │  │  │     │     │        │  │  │  │  ├── retry.py
   │  │  │     │     │        │  │  │  │  ├── ssltransport.py
   │  │  │     │     │        │  │  │  │  ├── ssl_.py
   │  │  │     │     │        │  │  │  │  ├── ssl_match_hostname.py
   │  │  │     │     │        │  │  │  │  ├── timeout.py
   │  │  │     │     │        │  │  │  │  ├── url.py
   │  │  │     │     │        │  │  │  │  ├── wait.py
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── _collections.py
   │  │  │     │     │        │  │  │  ├── _version.py
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── vendor.txt
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── __init__.py
   │  │  │     │     │        │  ├── __main__.py
   │  │  │     │     │        │  └── __pip-runner__.py
   │  │  │     │     │       ├── pip-25.2.dist-info
   │  │  │     │     │        │  ├── entry_points.txt
   │  │  │     │     │        │  ├── INSTALLER
   │  │  │     │     │        │  ├── licenses
   │  │  │     │     │        │  │  ├── AUTHORS.txt
   │  │  │     │     │        │  │  ├── LICENSE.txt
   │  │  │     │     │        │  │  └── src
   │  │  │     │     │        │  │    └── pip
   │  │  │     │     │        │  │       └── _vendor
   │  │  │     │     │        │  │          ├── cachecontrol
   │  │  │     │     │        │  │           │  └── LICENSE.txt
   │  │  │     │     │        │  │          ├── certifi
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── dependency_groups
   │  │  │     │     │        │  │           │  └── LICENSE.txt
   │  │  │     │     │        │  │          ├── distlib
   │  │  │     │     │        │  │           │  └── LICENSE.txt
   │  │  │     │     │        │  │          ├── distro
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── idna
   │  │  │     │     │        │  │           │  └── LICENSE.md
   │  │  │     │     │        │  │          ├── msgpack
   │  │  │     │     │        │  │           │  └── COPYING
   │  │  │     │     │        │  │          ├── packaging
   │  │  │     │     │        │  │           │  ├── LICENSE
   │  │  │     │     │        │  │           │  ├── LICENSE.APACHE
   │  │  │     │     │        │  │           │  └── LICENSE.BSD
   │  │  │     │     │        │  │          ├── pkg_resources
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── platformdirs
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── pygments
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── pyproject_hooks
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── requests
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── resolvelib
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── rich
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── tomli
   │  │  │     │     │        │  │           │  ├── LICENSE
   │  │  │     │     │        │  │           │  └── LICENSE-HEADER
   │  │  │     │     │        │  │          ├── tomli_w
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          ├── truststore
   │  │  │     │     │        │  │           │  └── LICENSE
   │  │  │     │     │        │  │          └── urllib3
   │  │  │     │     │        │  │             └── LICENSE.txt
   │  │  │     │     │        │  ├── METADATA
   │  │  │     │     │        │  ├── RECORD
   │  │  │     │     │        │  ├── REQUESTED
   │  │  │     │     │        │  ├── top_level.txt
   │  │  │     │     │        │  └── WHEEL
   │  │  │     │     │       ├── python_dateutil-2.9.0.post0.dist-info
   │  │  │     │     │        │  ├── INSTALLER
   │  │  │     │     │        │  ├── LICENSE
   │  │  │     │     │        │  ├── METADATA
   │  │  │     │     │        │  ├── RECORD
   │  │  │     │     │        │  ├── top_level.txt
   │  │  │     │     │        │  ├── WHEEL
   │  │  │     │     │        │  └── zip-safe
   │  │  │     │     │       ├── pytz
   │  │  │     │     │        │  ├── exceptions.py
   │  │  │     │     │        │  ├── lazy.py
   │  │  │     │     │        │  ├── reference.py
   │  │  │     │     │        │  ├── tzfile.py
   │  │  │     │     │        │  ├── tzinfo.py
   │  │  │     │     │        │  ├── zoneinfo
   │  │  │     │     │        │  │  ├── Africa
   │  │  │     │     │        │  │  │  ├── Abidjan
   │  │  │     │     │        │  │  │  ├── Accra
   │  │  │     │     │        │  │  │  ├── Addis_Ababa
   │  │  │     │     │        │  │  │  ├── Algiers
   │  │  │     │     │        │  │  │  ├── Asmara
   │  │  │     │     │        │  │  │  ├── Asmera
   │  │  │     │     │        │  │  │  ├── Bamako
   │  │  │     │     │        │  │  │  ├── Bangui
   │  │  │     │     │        │  │  │  ├── Banjul
   │  │  │     │     │        │  │  │  ├── Bissau
   │  │  │     │     │        │  │  │  ├── Blantyre
   │  │  │     │     │        │  │  │  ├── Brazzaville
   │  │  │     │     │        │  │  │  ├── Bujumbura
   │  │  │     │     │        │  │  │  ├── Cairo
   │  │  │     │     │        │  │  │  ├── Casablanca
   │  │  │     │     │        │  │  │  ├── Ceuta
   │  │  │     │     │        │  │  │  ├── Conakry
   │  │  │     │     │        │  │  │  ├── Dakar
   │  │  │     │     │        │  │  │  ├── Dar_es_Salaam
   │  │  │     │     │        │  │  │  ├── Djibouti
   │  │  │     │     │        │  │  │  ├── Douala
   │  │  │     │     │        │  │  │  ├── El_Aaiun
   │  │  │     │     │        │  │  │  ├── Freetown
   │  │  │     │     │        │  │  │  ├── Gaborone
   │  │  │     │     │        │  │  │  ├── Harare
   │  │  │     │     │        │  │  │  ├── Johannesburg
   │  │  │     │     │        │  │  │  ├── Juba
   │  │  │     │     │        │  │  │  ├── Kampala
   │  │  │     │     │        │  │  │  ├── Khartoum
   │  │  │     │     │        │  │  │  ├── Kigali
   │  │  │     │     │        │  │  │  ├── Kinshasa
   │  │  │     │     │        │  │  │  ├── Lagos
   │  │  │     │     │        │  │  │  ├── Libreville
   │  │  │     │     │        │  │  │  ├── Lome
   │  │  │     │     │        │  │  │  ├── Luanda
   │  │  │     │     │        │  │  │  ├── Lubumbashi
   │  │  │     │     │        │  │  │  ├── Lusaka
   │  │  │     │     │        │  │  │  ├── Malabo
   │  │  │     │     │        │  │  │  ├── Maputo
   │  │  │     │     │        │  │  │  ├── Maseru
   │  │  │     │     │        │  │  │  ├── Mbabane
   │  │  │     │     │        │  │  │  ├── Mogadishu
   │  │  │     │     │        │  │  │  ├── Monrovia
   │  │  │     │     │        │  │  │  ├── Nairobi
   │  │  │     │     │        │  │  │  ├── Ndjamena
   │  │  │     │     │        │  │  │  ├── Niamey
   │  │  │     │     │        │  │  │  ├── Nouakchott
   │  │  │     │     │        │  │  │  ├── Ouagadougou
   │  │  │     │     │        │  │  │  ├── Porto-Novo
   │  │  │     │     │        │  │  │  ├── Sao_Tome
   │  │  │     │     │        │  │  │  ├── Timbuktu
   │  │  │     │     │        │  │  │  ├── Tripoli
   │  │  │     │     │        │  │  │  ├── Tunis
   │  │  │     │     │        │  │  │  └── Windhoek
   │  │  │     │     │        │  │  ├── America
   │  │  │     │     │        │  │  │  ├── Adak
   │  │  │     │     │        │  │  │  ├── Anchorage
   │  │  │     │     │        │  │  │  ├── Anguilla
   │  │  │     │     │        │  │  │  ├── Antigua
   │  │  │     │     │        │  │  │  ├── Araguaina
   │  │  │     │     │        │  │  │  ├── Argentina
   │  │  │     │     │        │  │  │  │  ├── Buenos_Aires
   │  │  │     │     │        │  │  │  │  ├── Catamarca
   │  │  │     │     │        │  │  │  │  ├── ComodRivadavia
   │  │  │     │     │        │  │  │  │  ├── Cordoba
   │  │  │     │     │        │  │  │  │  ├── Jujuy
   │  │  │     │     │        │  │  │  │  ├── La_Rioja
   │  │  │     │     │        │  │  │  │  ├── Mendoza
   │  │  │     │     │        │  │  │  │  ├── Rio_Gallegos
   │  │  │     │     │        │  │  │  │  ├── Salta
   │  │  │     │     │        │  │  │  │  ├── San_Juan
   │  │  │     │     │        │  │  │  │  ├── San_Luis
   │  │  │     │     │        │  │  │  │  ├── Tucuman
   │  │  │     │     │        │  │  │  │  └── Ushuaia
   │  │  │     │     │        │  │  │  ├── Aruba
   │  │  │     │     │        │  │  │  ├── Asuncion
   │  │  │     │     │        │  │  │  ├── Atikokan
   │  │  │     │     │        │  │  │  ├── Atka
   │  │  │     │     │        │  │  │  ├── Bahia
   │  │  │     │     │        │  │  │  ├── Bahia_Banderas
   │  │  │     │     │        │  │  │  ├── Barbados
   │  │  │     │     │        │  │  │  ├── Belem
   │  │  │     │     │        │  │  │  ├── Belize
   │  │  │     │     │        │  │  │  ├── Blanc-Sablon
   │  │  │     │     │        │  │  │  ├── Boa_Vista
   │  │  │     │     │        │  │  │  ├── Bogota
   │  │  │     │     │        │  │  │  ├── Boise
   │  │  │     │     │        │  │  │  ├── Buenos_Aires
   │  │  │     │     │        │  │  │  ├── Cambridge_Bay
   │  │  │     │     │        │  │  │  ├── Campo_Grande
   │  │  │     │     │        │  │  │  ├── Cancun
   │  │  │     │     │        │  │  │  ├── Caracas
   │  │  │     │     │        │  │  │  ├── Catamarca
   │  │  │     │     │        │  │  │  ├── Cayenne
   │  │  │     │     │        │  │  │  ├── Cayman
   │  │  │     │     │        │  │  │  ├── Chicago
   │  │  │     │     │        │  │  │  ├── Chihuahua
   │  │  │     │     │        │  │  │  ├── Ciudad_Juarez
   │  │  │     │     │        │  │  │  ├── Coral_Harbour
   │  │  │     │     │        │  │  │  ├── Cordoba
   │  │  │     │     │        │  │  │  ├── Costa_Rica
   │  │  │     │     │        │  │  │  ├── Coyhaique
   │  │  │     │     │        │  │  │  ├── Creston
   │  │  │     │     │        │  │  │  ├── Cuiaba
   │  │  │     │     │        │  │  │  ├── Curacao
   │  │  │     │     │        │  │  │  ├── Danmarkshavn
   │  │  │     │     │        │  │  │  ├── Dawson
   │  │  │     │     │        │  │  │  ├── Dawson_Creek
   │  │  │     │     │        │  │  │  ├── Denver
   │  │  │     │     │        │  │  │  ├── Detroit
   │  │  │     │     │        │  │  │  ├── Dominica
   │  │  │     │     │        │  │  │  ├── Edmonton
   │  │  │     │     │        │  │  │  ├── Eirunepe
   │  │  │     │     │        │  │  │  ├── El_Salvador
   │  │  │     │     │        │  │  │  ├── Ensenada
   │  │  │     │     │        │  │  │  ├── Fortaleza
   │  │  │     │     │        │  │  │  ├── Fort_Nelson
   │  │  │     │     │        │  │  │  ├── Fort_Wayne
   │  │  │     │     │        │  │  │  ├── Glace_Bay
   │  │  │     │     │        │  │  │  ├── Godthab
   │  │  │     │     │        │  │  │  ├── Goose_Bay
   │  │  │     │     │        │  │  │  ├── Grand_Turk
   │  │  │     │     │        │  │  │  ├── Grenada
   │  │  │     │     │        │  │  │  ├── Guadeloupe
   │  │  │     │     │        │  │  │  ├── Guatemala
   │  │  │     │     │        │  │  │  ├── Guayaquil
   │  │  │     │     │        │  │  │  ├── Guyana
   │  │  │     │     │        │  │  │  ├── Halifax
   │  │  │     │     │        │  │  │  ├── Havana
   │  │  │     │     │        │  │  │  ├── Hermosillo
   │  │  │     │     │        │  │  │  ├── Indiana
   │  │  │     │     │        │  │  │  │  ├── Indianapolis
   │  │  │     │     │        │  │  │  │  ├── Knox
   │  │  │     │     │        │  │  │  │  ├── Marengo
   │  │  │     │     │        │  │  │  │  ├── Petersburg
   │  │  │     │     │        │  │  │  │  ├── Tell_City
   │  │  │     │     │        │  │  │  │  ├── Vevay
   │  │  │     │     │        │  │  │  │  ├── Vincennes
   │  │  │     │     │        │  │  │  │  └── Winamac
   │  │  │     │     │        │  │  │  ├── Indianapolis
   │  │  │     │     │        │  │  │  ├── Inuvik
   │  │  │     │     │        │  │  │  ├── Iqaluit
   │  │  │     │     │        │  │  │  ├── Jamaica
   │  │  │     │     │        │  │  │  ├── Jujuy
   │  │  │     │     │        │  │  │  ├── Juneau
   │  │  │     │     │        │  │  │  ├── Kentucky
   │  │  │     │     │        │  │  │  │  ├── Louisville
   │  │  │     │     │        │  │  │  │  └── Monticello
   │  │  │     │     │        │  │  │  ├── Knox_IN
   │  │  │     │     │        │  │  │  ├── Kralendijk
   │  │  │     │     │        │  │  │  ├── La_Paz
   │  │  │     │     │        │  │  │  ├── Lima
   │  │  │     │     │        │  │  │  ├── Los_Angeles
   │  │  │     │     │        │  │  │  ├── Louisville
   │  │  │     │     │        │  │  │  ├── Lower_Princes
   │  │  │     │     │        │  │  │  ├── Maceio
   │  │  │     │     │        │  │  │  ├── Managua
   │  │  │     │     │        │  │  │  ├── Manaus
   │  │  │     │     │        │  │  │  ├── Marigot
   │  │  │     │     │        │  │  │  ├── Martinique
   │  │  │     │     │        │  │  │  ├── Matamoros
   │  │  │     │     │        │  │  │  ├── Mazatlan
   │  │  │     │     │        │  │  │  ├── Mendoza
   │  │  │     │     │        │  │  │  ├── Menominee
   │  │  │     │     │        │  │  │  ├── Merida
   │  │  │     │     │        │  │  │  ├── Metlakatla
   │  │  │     │     │        │  │  │  ├── Mexico_City
   │  │  │     │     │        │  │  │  ├── Miquelon
   │  │  │     │     │        │  │  │  ├── Moncton
   │  │  │     │     │        │  │  │  ├── Monterrey
   │  │  │     │     │        │  │  │  ├── Montevideo
   │  │  │     │     │        │  │  │  ├── Montreal
   │  │  │     │     │        │  │  │  ├── Montserrat
   │  │  │     │     │        │  │  │  ├── Nassau
   │  │  │     │     │        │  │  │  ├── New_York
   │  │  │     │     │        │  │  │  ├── Nipigon
   │  │  │     │     │        │  │  │  ├── Nome
   │  │  │     │     │        │  │  │  ├── Noronha
   │  │  │     │     │        │  │  │  ├── North_Dakota
   │  │  │     │     │        │  │  │  │  ├── Beulah
   │  │  │     │     │        │  │  │  │  ├── Center
   │  │  │     │     │        │  │  │  │  └── New_Salem
   │  │  │     │     │        │  │  │  ├── Nuuk
   │  │  │     │     │        │  │  │  ├── Ojinaga
   │  │  │     │     │        │  │  │  ├── Panama
   │  │  │     │     │        │  │  │  ├── Pangnirtung
   │  │  │     │     │        │  │  │  ├── Paramaribo
   │  │  │     │     │        │  │  │  ├── Phoenix
   │  │  │     │     │        │  │  │  ├── Port-au-Prince
   │  │  │     │     │        │  │  │  ├── Porto_Acre
   │  │  │     │     │        │  │  │  ├── Porto_Velho
   │  │  │     │     │        │  │  │  ├── Port_of_Spain
   │  │  │     │     │        │  │  │  ├── Puerto_Rico
   │  │  │     │     │        │  │  │  ├── Punta_Arenas
   │  │  │     │     │        │  │  │  ├── Rainy_River
   │  │  │     │     │        │  │  │  ├── Rankin_Inlet
   │  │  │     │     │        │  │  │  ├── Recife
   │  │  │     │     │        │  │  │  ├── Regina
   │  │  │     │     │        │  │  │  ├── Resolute
   │  │  │     │     │        │  │  │  ├── Rio_Branco
   │  │  │     │     │        │  │  │  ├── Rosario
   │  │  │     │     │        │  │  │  ├── Santarem
   │  │  │     │     │        │  │  │  ├── Santa_Isabel
   │  │  │     │     │        │  │  │  ├── Santiago
   │  │  │     │     │        │  │  │  ├── Santo_Domingo
   │  │  │     │     │        │  │  │  ├── Sao_Paulo
   │  │  │     │     │        │  │  │  ├── Scoresbysund
   │  │  │     │     │        │  │  │  ├── Shiprock
   │  │  │     │     │        │  │  │  ├── Sitka
   │  │  │     │     │        │  │  │  ├── St_Barthelemy
   │  │  │     │     │        │  │  │  ├── St_Johns
   │  │  │     │     │        │  │  │  ├── St_Kitts
   │  │  │     │     │        │  │  │  ├── St_Lucia
   │  │  │     │     │        │  │  │  ├── St_Thomas
   │  │  │     │     │        │  │  │  ├── St_Vincent
   │  │  │     │     │        │  │  │  ├── Swift_Current
   │  │  │     │     │        │  │  │  ├── Tegucigalpa
   │  │  │     │     │        │  │  │  ├── Thule
   │  │  │     │     │        │  │  │  ├── Thunder_Bay
   │  │  │     │     │        │  │  │  ├── Tijuana
   │  │  │     │     │        │  │  │  ├── Toronto
   │  │  │     │     │        │  │  │  ├── Tortola
   │  │  │     │     │        │  │  │  ├── Vancouver
   │  │  │     │     │        │  │  │  ├── Virgin
   │  │  │     │     │        │  │  │  ├── Whitehorse
   │  │  │     │     │        │  │  │  ├── Winnipeg
   │  │  │     │     │        │  │  │  ├── Yakutat
   │  │  │     │     │        │  │  │  └── Yellowknife
   │  │  │     │     │        │  │  ├── Antarctica
   │  │  │     │     │        │  │  │  ├── Casey
   │  │  │     │     │        │  │  │  ├── Davis
   │  │  │     │     │        │  │  │  ├── DumontDUrville
   │  │  │     │     │        │  │  │  ├── Macquarie
   │  │  │     │     │        │  │  │  ├── Mawson
   │  │  │     │     │        │  │  │  ├── McMurdo
   │  │  │     │     │        │  │  │  ├── Palmer
   │  │  │     │     │        │  │  │  ├── Rothera
   │  │  │     │     │        │  │  │  ├── South_Pole
   │  │  │     │     │        │  │  │  ├── Syowa
   │  │  │     │     │        │  │  │  ├── Troll
   │  │  │     │     │        │  │  │  └── Vostok
   │  │  │     │     │        │  │  ├── Arctic
   │  │  │     │     │        │  │  │  └── Longyearbyen
   │  │  │     │     │        │  │  ├── Asia
   │  │  │     │     │        │  │  │  ├── Aden
   │  │  │     │     │        │  │  │  ├── Almaty
   │  │  │     │     │        │  │  │  ├── Amman
   │  │  │     │     │        │  │  │  ├── Anadyr
   │  │  │     │     │        │  │  │  ├── Aqtau
   │  │  │     │     │        │  │  │  ├── Aqtobe
   │  │  │     │     │        │  │  │  ├── Ashgabat
   │  │  │     │     │        │  │  │  ├── Ashkhabad
   │  │  │     │     │        │  │  │  ├── Atyrau
   │  │  │     │     │        │  │  │  ├── Baghdad
   │  │  │     │     │        │  │  │  ├── Bahrain
   │  │  │     │     │        │  │  │  ├── Baku
   │  │  │     │     │        │  │  │  ├── Bangkok
   │  │  │     │     │        │  │  │  ├── Barnaul
   │  │  │     │     │        │  │  │  ├── Beirut
   │  │  │     │     │        │  │  │  ├── Bishkek
   │  │  │     │     │        │  │  │  ├── Brunei
   │  │  │     │     │        │  │  │  ├── Calcutta
   │  │  │     │     │        │  │  │  ├── Chita
   │  │  │     │     │        │  │  │  ├── Choibalsan
   │  │  │     │     │        │  │  │  ├── Chongqing
   │  │  │     │     │        │  │  │  ├── Chungking
   │  │  │     │     │        │  │  │  ├── Colombo
   │  │  │     │     │        │  │  │  ├── Dacca
   │  │  │     │     │        │  │  │  ├── Damascus
   │  │  │     │     │        │  │  │  ├── Dhaka
   │  │  │     │     │        │  │  │  ├── Dili
   │  │  │     │     │        │  │  │  ├── Dubai
   │  │  │     │     │        │  │  │  ├── Dushanbe
   │  │  │     │     │        │  │  │  ├── Famagusta
   │  │  │     │     │        │  │  │  ├── Gaza
   │  │  │     │     │        │  │  │  ├── Harbin
   │  │  │     │     │        │  │  │  ├── Hebron
   │  │  │     │     │        │  │  │  ├── Hong_Kong
   │  │  │     │     │        │  │  │  ├── Hovd
   │  │  │     │     │        │  │  │  ├── Ho_Chi_Minh
   │  │  │     │     │        │  │  │  ├── Irkutsk
   │  │  │     │     │        │  │  │  ├── Istanbul
   │  │  │     │     │        │  │  │  ├── Jakarta
   │  │  │     │     │        │  │  │  ├── Jayapura
   │  │  │     │     │        │  │  │  ├── Jerusalem
   │  │  │     │     │        │  │  │  ├── Kabul
   │  │  │     │     │        │  │  │  ├── Kamchatka
   │  │  │     │     │        │  │  │  ├── Karachi
   │  │  │     │     │        │  │  │  ├── Kashgar
   │  │  │     │     │        │  │  │  ├── Kathmandu
   │  │  │     │     │        │  │  │  ├── Katmandu
   │  │  │     │     │        │  │  │  ├── Khandyga
   │  │  │     │     │        │  │  │  ├── Kolkata
   │  │  │     │     │        │  │  │  ├── Krasnoyarsk
   │  │  │     │     │        │  │  │  ├── Kuala_Lumpur
   │  │  │     │     │        │  │  │  ├── Kuching
   │  │  │     │     │        │  │  │  ├── Kuwait
   │  │  │     │     │        │  │  │  ├── Macao
   │  │  │     │     │        │  │  │  ├── Macau
   │  │  │     │     │        │  │  │  ├── Magadan
   │  │  │     │     │        │  │  │  ├── Makassar
   │  │  │     │     │        │  │  │  ├── Manila
   │  │  │     │     │        │  │  │  ├── Muscat
   │  │  │     │     │        │  │  │  ├── Nicosia
   │  │  │     │     │        │  │  │  ├── Novokuznetsk
   │  │  │     │     │        │  │  │  ├── Novosibirsk
   │  │  │     │     │        │  │  │  ├── Omsk
   │  │  │     │     │        │  │  │  ├── Oral
   │  │  │     │     │        │  │  │  ├── Phnom_Penh
   │  │  │     │     │        │  │  │  ├── Pontianak
   │  │  │     │     │        │  │  │  ├── Pyongyang
   │  │  │     │     │        │  │  │  ├── Qatar
   │  │  │     │     │        │  │  │  ├── Qostanay
   │  │  │     │     │        │  │  │  ├── Qyzylorda
   │  │  │     │     │        │  │  │  ├── Rangoon
   │  │  │     │     │        │  │  │  ├── Riyadh
   │  │  │     │     │        │  │  │  ├── Saigon
   │  │  │     │     │        │  │  │  ├── Sakhalin
   │  │  │     │     │        │  │  │  ├── Samarkand
   │  │  │     │     │        │  │  │  ├── Seoul
   │  │  │     │     │        │  │  │  ├── Shanghai
   │  │  │     │     │        │  │  │  ├── Singapore
   │  │  │     │     │        │  │  │  ├── Srednekolymsk
   │  │  │     │     │        │  │  │  ├── Taipei
   │  │  │     │     │        │  │  │  ├── Tashkent
   │  │  │     │     │        │  │  │  ├── Tbilisi
   │  │  │     │     │        │  │  │  ├── Tehran
   │  │  │     │     │        │  │  │  ├── Tel_Aviv
   │  │  │     │     │        │  │  │  ├── Thimbu
   │  │  │     │     │        │  │  │  ├── Thimphu
   │  │  │     │     │        │  │  │  ├── Tokyo
   │  │  │     │     │        │  │  │  ├── Tomsk
   │  │  │     │     │        │  │  │  ├── Ujung_Pandang
   │  │  │     │     │        │  │  │  ├── Ulaanbaatar
   │  │  │     │     │        │  │  │  ├── Ulan_Bator
   │  │  │     │     │        │  │  │  ├── Urumqi
   │  │  │     │     │        │  │  │  ├── Ust-Nera
   │  │  │     │     │        │  │  │  ├── Vientiane
   │  │  │     │     │        │  │  │  ├── Vladivostok
   │  │  │     │     │        │  │  │  ├── Yakutsk
   │  │  │     │     │        │  │  │  ├── Yangon
   │  │  │     │     │        │  │  │  ├── Yekaterinburg
   │  │  │     │     │        │  │  │  └── Yerevan
   │  │  │     │     │        │  │  ├── Atlantic
   │  │  │     │     │        │  │  │  ├── Azores
   │  │  │     │     │        │  │  │  ├── Bermuda
   │  │  │     │     │        │  │  │  ├── Canary
   │  │  │     │     │        │  │  │  ├── Cape_Verde
   │  │  │     │     │        │  │  │  ├── Faeroe
   │  │  │     │     │        │  │  │  ├── Faroe
   │  │  │     │     │        │  │  │  ├── Jan_Mayen
   │  │  │     │     │        │  │  │  ├── Madeira
   │  │  │     │     │        │  │  │  ├── Reykjavik
   │  │  │     │     │        │  │  │  ├── South_Georgia
   │  │  │     │     │        │  │  │  ├── Stanley
   │  │  │     │     │        │  │  │  └── St_Helena
   │  │  │     │     │        │  │  ├── Australia
   │  │  │     │     │        │  │  │  ├── ACT
   │  │  │     │     │        │  │  │  ├── Adelaide
   │  │  │     │     │        │  │  │  ├── Brisbane
   │  │  │     │     │        │  │  │  ├── Broken_Hill
   │  │  │     │     │        │  │  │  ├── Canberra
   │  │  │     │     │        │  │  │  ├── Currie
   │  │  │     │     │        │  │  │  ├── Darwin
   │  │  │     │     │        │  │  │  ├── Eucla
   │  │  │     │     │        │  │  │  ├── Hobart
   │  │  │     │     │        │  │  │  ├── LHI
   │  │  │     │     │        │  │  │  ├── Lindeman
   │  │  │     │     │        │  │  │  ├── Lord_Howe
   │  │  │     │     │        │  │  │  ├── Melbourne
   │  │  │     │     │        │  │  │  ├── North
   │  │  │     │     │        │  │  │  ├── NSW
   │  │  │     │     │        │  │  │  ├── Perth
   │  │  │     │     │        │  │  │  ├── Queensland
   │  │  │     │     │        │  │  │  ├── South
   │  │  │     │     │        │  │  │  ├── Sydney
   │  │  │     │     │        │  │  │  ├── Tasmania
   │  │  │     │     │        │  │  │  ├── Victoria
   │  │  │     │     │        │  │  │  ├── West
   │  │  │     │     │        │  │  │  └── Yancowinna
   │  │  │     │     │        │  │  ├── Brazil
   │  │  │     │     │        │  │  │  ├── Acre
   │  │  │     │     │        │  │  │  ├── DeNoronha
   │  │  │     │     │        │  │  │  ├── East
   │  │  │     │     │        │  │  │  └── West
   │  │  │     │     │        │  │  ├── Canada
   │  │  │     │     │        │  │  │  ├── Atlantic
   │  │  │     │     │        │  │  │  ├── Central
   │  │  │     │     │        │  │  │  ├── Eastern
   │  │  │     │     │        │  │  │  ├── Mountain
   │  │  │     │     │        │  │  │  ├── Newfoundland
   │  │  │     │     │        │  │  │  ├── Pacific
   │  │  │     │     │        │  │  │  ├── Saskatchewan
   │  │  │     │     │        │  │  │  └── Yukon
   │  │  │     │     │        │  │  ├── CET
   │  │  │     │     │        │  │  ├── Chile
   │  │  │     │     │        │  │  │  ├── Continental
   │  │  │     │     │        │  │  │  └── EasterIsland
   │  │  │     │     │        │  │  ├── CST6CDT
   │  │  │     │     │        │  │  ├── Cuba
   │  │  │     │     │        │  │  ├── EET
   │  │  │     │     │        │  │  ├── Egypt
   │  │  │     │     │        │  │  ├── Eire
   │  │  │     │     │        │  │  ├── EST
   │  │  │     │     │        │  │  ├── EST5EDT
   │  │  │     │     │        │  │  ├── Etc
   │  │  │     │     │        │  │  │  ├── GMT
   │  │  │     │     │        │  │  │  ├── GMT+0
   │  │  │     │     │        │  │  │  ├── GMT+1
   │  │  │     │     │        │  │  │  ├── GMT+10
   │  │  │     │     │        │  │  │  ├── GMT+11
   │  │  │     │     │        │  │  │  ├── GMT+12
   │  │  │     │     │        │  │  │  ├── GMT+2
   │  │  │     │     │        │  │  │  ├── GMT+3
   │  │  │     │     │        │  │  │  ├── GMT+4
   │  │  │     │     │        │  │  │  ├── GMT+5
   │  │  │     │     │        │  │  │  ├── GMT+6
   │  │  │     │     │        │  │  │  ├── GMT+7
   │  │  │     │     │        │  │  │  ├── GMT+8
   │  │  │     │     │        │  │  │  ├── GMT+9
   │  │  │     │     │        │  │  │  ├── GMT-0
   │  │  │     │     │        │  │  │  ├── GMT-1
   │  │  │     │     │        │  │  │  ├── GMT-10
   │  │  │     │     │        │  │  │  ├── GMT-11
   │  │  │     │     │        │  │  │  ├── GMT-12
   │  │  │     │     │        │  │  │  ├── GMT-13
   │  │  │     │     │        │  │  │  ├── GMT-14
   │  │  │     │     │        │  │  │  ├── GMT-2
   │  │  │     │     │        │  │  │  ├── GMT-3
   │  │  │     │     │        │  │  │  ├── GMT-4
   │  │  │     │     │        │  │  │  ├── GMT-5
   │  │  │     │     │        │  │  │  ├── GMT-6
   │  │  │     │     │        │  │  │  ├── GMT-7
   │  │  │     │     │        │  │  │  ├── GMT-8
   │  │  │     │     │        │  │  │  ├── GMT-9
   │  │  │     │     │        │  │  │  ├── GMT0
   │  │  │     │     │        │  │  │  ├── Greenwich
   │  │  │     │     │        │  │  │  ├── UCT
   │  │  │     │     │        │  │  │  ├── Universal
   │  │  │     │     │        │  │  │  ├── UTC
   │  │  │     │     │        │  │  │  └── Zulu
   │  │  │     │     │        │  │  ├── Europe
   │  │  │     │     │        │  │  │  ├── Amsterdam
   │  │  │     │     │        │  │  │  ├── Andorra
   │  │  │     │     │        │  │  │  ├── Astrakhan
   │  │  │     │     │        │  │  │  ├── Athens
   │  │  │     │     │        │  │  │  ├── Belfast
   │  │  │     │     │        │  │  │  ├── Belgrade
   │  │  │     │     │        │  │  │  ├── Berlin
   │  │  │     │     │        │  │  │  ├── Bratislava
   │  │  │     │     │        │  │  │  ├── Brussels
   │  │  │     │     │        │  │  │  ├── Bucharest
   │  │  │     │     │        │  │  │  ├── Budapest
   │  │  │     │     │        │  │  │  ├── Busingen
   │  │  │     │     │        │  │  │  ├── Chisinau
   │  │  │     │     │        │  │  │  ├── Copenhagen
   │  │  │     │     │        │  │  │  ├── Dublin
   │  │  │     │     │        │  │  │  ├── Gibraltar
   │  │  │     │     │        │  │  │  ├── Guernsey
   │  │  │     │     │        │  │  │  ├── Helsinki
   │  │  │     │     │        │  │  │  ├── Isle_of_Man
   │  │  │     │     │        │  │  │  ├── Istanbul
   │  │  │     │     │        │  │  │  ├── Jersey
   │  │  │     │     │        │  │  │  ├── Kaliningrad
   │  │  │     │     │        │  │  │  ├── Kiev
   │  │  │     │     │        │  │  │  ├── Kirov
   │  │  │     │     │        │  │  │  ├── Kyiv
   │  │  │     │     │        │  │  │  ├── Lisbon
   │  │  │     │     │        │  │  │  ├── Ljubljana
   │  │  │     │     │        │  │  │  ├── London
   │  │  │     │     │        │  │  │  ├── Luxembourg
   │  │  │     │     │        │  │  │  ├── Madrid
   │  │  │     │     │        │  │  │  ├── Malta
   │  │  │     │     │        │  │  │  ├── Mariehamn
   │  │  │     │     │        │  │  │  ├── Minsk
   │  │  │     │     │        │  │  │  ├── Monaco
   │  │  │     │     │        │  │  │  ├── Moscow
   │  │  │     │     │        │  │  │  ├── Nicosia
   │  │  │     │     │        │  │  │  ├── Oslo
   │  │  │     │     │        │  │  │  ├── Paris
   │  │  │     │     │        │  │  │  ├── Podgorica
   │  │  │     │     │        │  │  │  ├── Prague
   │  │  │     │     │        │  │  │  ├── Riga
   │  │  │     │     │        │  │  │  ├── Rome
   │  │  │     │     │        │  │  │  ├── Samara
   │  │  │     │     │        │  │  │  ├── San_Marino
   │  │  │     │     │        │  │  │  ├── Sarajevo
   │  │  │     │     │        │  │  │  ├── Saratov
   │  │  │     │     │        │  │  │  ├── Simferopol
   │  │  │     │     │        │  │  │  ├── Skopje
   │  │  │     │     │        │  │  │  ├── Sofia
   │  │  │     │     │        │  │  │  ├── Stockholm
   │  │  │     │     │        │  │  │  ├── Tallinn
   │  │  │     │     │        │  │  │  ├── Tirane
   │  │  │     │     │        │  │  │  ├── Tiraspol
   │  │  │     │     │        │  │  │  ├── Ulyanovsk
   │  │  │     │     │        │  │  │  ├── Uzhgorod
   │  │  │     │     │        │  │  │  ├── Vaduz
   │  │  │     │     │        │  │  │  ├── Vatican
   │  │  │     │     │        │  │  │  ├── Vienna
   │  │  │     │     │        │  │  │  ├── Vilnius
   │  │  │     │     │        │  │  │  ├── Volgograd
   │  │  │     │     │        │  │  │  ├── Warsaw
   │  │  │     │     │        │  │  │  ├── Zagreb
   │  │  │     │     │        │  │  │  ├── Zaporozhye
   │  │  │     │     │        │  │  │  └── Zurich
   │  │  │     │     │        │  │  ├── Factory
   │  │  │     │     │        │  │  ├── GB
   │  │  │     │     │        │  │  ├── GB-Eire
   │  │  │     │     │        │  │  ├── GMT
   │  │  │     │     │        │  │  ├── GMT+0
   │  │  │     │     │        │  │  ├── GMT-0
   │  │  │     │     │        │  │  ├── GMT0
   │  │  │     │     │        │  │  ├── Greenwich
   │  │  │     │     │        │  │  ├── Hongkong
   │  │  │     │     │        │  │  ├── HST
   │  │  │     │     │        │  │  ├── Iceland
   │  │  │     │     │        │  │  ├── Indian
   │  │  │     │     │        │  │  │  ├── Antananarivo
   │  │  │     │     │        │  │  │  ├── Chagos
   │  │  │     │     │        │  │  │  ├── Christmas
   │  │  │     │     │        │  │  │  ├── Cocos
   │  │  │     │     │        │  │  │  ├── Comoro
   │  │  │     │     │        │  │  │  ├── Kerguelen
   │  │  │     │     │        │  │  │  ├── Mahe
   │  │  │     │     │        │  │  │  ├── Maldives
   │  │  │     │     │        │  │  │  ├── Mauritius
   │  │  │     │     │        │  │  │  ├── Mayotte
   │  │  │     │     │        │  │  │  └── Reunion
   │  │  │     │     │        │  │  ├── Iran
   │  │  │     │     │        │  │  ├── iso3166.tab
   │  │  │     │     │        │  │  ├── Israel
   │  │  │     │     │        │  │  ├── Jamaica
   │  │  │     │     │        │  │  ├── Japan
   │  │  │     │     │        │  │  ├── Kwajalein
   │  │  │     │     │        │  │  ├── leapseconds
   │  │  │     │     │        │  │  ├── Libya
   │  │  │     │     │        │  │  ├── MET
   │  │  │     │     │        │  │  ├── Mexico
   │  │  │     │     │        │  │  │  ├── BajaNorte
   │  │  │     │     │        │  │  │  ├── BajaSur
   │  │  │     │     │        │  │  │  └── General
   │  │  │     │     │        │  │  ├── MST
   │  │  │     │     │        │  │  ├── MST7MDT
   │  │  │     │     │        │  │  ├── Navajo
   │  │  │     │     │        │  │  ├── NZ
   │  │  │     │     │        │  │  ├── NZ-CHAT
   │  │  │     │     │        │  │  ├── Pacific
   │  │  │     │     │        │  │  │  ├── Apia
   │  │  │     │     │        │  │  │  ├── Auckland
   │  │  │     │     │        │  │  │  ├── Bougainville
   │  │  │     │     │        │  │  │  ├── Chatham
   │  │  │     │     │        │  │  │  ├── Chuuk
   │  │  │     │     │        │  │  │  ├── Easter
   │  │  │     │     │        │  │  │  ├── Efate
   │  │  │     │     │        │  │  │  ├── Enderbury
   │  │  │     │     │        │  │  │  ├── Fakaofo
   │  │  │     │     │        │  │  │  ├── Fiji
   │  │  │     │     │        │  │  │  ├── Funafuti
   │  │  │     │     │        │  │  │  ├── Galapagos
   │  │  │     │     │        │  │  │  ├── Gambier
   │  │  │     │     │        │  │  │  ├── Guadalcanal
   │  │  │     │     │        │  │  │  ├── Guam
   │  │  │     │     │        │  │  │  ├── Honolulu
   │  │  │     │     │        │  │  │  ├── Johnston
   │  │  │     │     │        │  │  │  ├── Kanton
   │  │  │     │     │        │  │  │  ├── Kiritimati
   │  │  │     │     │        │  │  │  ├── Kosrae
   │  │  │     │     │        │  │  │  ├── Kwajalein
   │  │  │     │     │        │  │  │  ├── Majuro
   │  │  │     │     │        │  │  │  ├── Marquesas
   │  │  │     │     │        │  │  │  ├── Midway
   │  │  │     │     │        │  │  │  ├── Nauru
   │  │  │     │     │        │  │  │  ├── Niue
   │  │  │     │     │        │  │  │  ├── Norfolk
   │  │  │     │     │        │  │  │  ├── Noumea
   │  │  │     │     │        │  │  │  ├── Pago_Pago
   │  │  │     │     │        │  │  │  ├── Palau
   │  │  │     │     │        │  │  │  ├── Pitcairn
   │  │  │     │     │        │  │  │  ├── Pohnpei
   │  │  │     │     │        │  │  │  ├── Ponape
   │  │  │     │     │        │  │  │  ├── Port_Moresby
   │  │  │     │     │        │  │  │  ├── Rarotonga
   │  │  │     │     │        │  │  │  ├── Saipan
   │  │  │     │     │        │  │  │  ├── Samoa
   │  │  │     │     │        │  │  │  ├── Tahiti
   │  │  │     │     │        │  │  │  ├── Tarawa
   │  │  │     │     │        │  │  │  ├── Tongatapu
   │  │  │     │     │        │  │  │  ├── Truk
   │  │  │     │     │        │  │  │  ├── Wake
   │  │  │     │     │        │  │  │  ├── Wallis
   │  │  │     │     │        │  │  │  └── Yap
   │  │  │     │     │        │  │  ├── Poland
   │  │  │     │     │        │  │  ├── Portugal
   │  │  │     │     │        │  │  ├── PRC
   │  │  │     │     │        │  │  ├── PST8PDT
   │  │  │     │     │        │  │  ├── ROC
   │  │  │     │     │        │  │  ├── ROK
   │  │  │     │     │        │  │  ├── Singapore
   │  │  │     │     │        │  │  ├── Turkey
   │  │  │     │     │        │  │  ├── tzdata.zi
   │  │  │     │     │        │  │  ├── UCT
   │  │  │     │     │        │  │  ├── Universal
   │  │  │     │     │        │  │  ├── US
   │  │  │     │     │        │  │  │  ├── Alaska
   │  │  │     │     │        │  │  │  ├── Aleutian
   │  │  │     │     │        │  │  │  ├── Arizona
   │  │  │     │     │        │  │  │  ├── Central
   │  │  │     │     │        │  │  │  ├── East-Indiana
   │  │  │     │     │        │  │  │  ├── Eastern
   │  │  │     │     │        │  │  │  ├── Hawaii
   │  │  │     │     │        │  │  │  ├── Indiana-Starke
   │  │  │     │     │        │  │  │  ├── Michigan
   │  │  │     │     │        │  │  │  ├── Mountain
   │  │  │     │     │        │  │  │  ├── Pacific
   │  │  │     │     │        │  │  │  └── Samoa
   │  │  │     │     │        │  │  ├── UTC
   │  │  │     │     │        │  │  ├── W-SU
   │  │  │     │     │        │  │  ├── WET
   │  │  │     │     │        │  │  ├── zone.tab
   │  │  │     │     │        │  │  ├── zone1970.tab
   │  │  │     │     │        │  │  ├── zonenow.tab
   │  │  │     │     │        │  │  └── Zulu
   │  │  │     │     │        │  └── __init__.py
   │  │  │     │     │       ├── pytz-2025.2.dist-info
   │  │  │     │     │        │  ├── INSTALLER
   │  │  │     │     │        │  ├── LICENSE.txt
   │  │  │     │     │        │  ├── METADATA
   │  │  │     │     │        │  ├── RECORD
   │  │  │     │     │        │  ├── top_level.txt
   │  │  │     │     │        │  ├── WHEEL
   │  │  │     │     │        │  └── zip-safe
   │  │  │     │     │       ├── six-1.17.0.dist-info
   │  │  │     │     │        │  ├── INSTALLER
   │  │  │     │     │        │  ├── LICENSE
   │  │  │     │     │        │  ├── METADATA
   │  │  │     │     │        │  ├── RECORD
   │  │  │     │     │        │  ├── top_level.txt
   │  │  │     │     │        │  └── WHEEL
   │  │  │     │     │       ├── six.py
   │  │  │     │     │       ├── tzdata
   │  │  │     │     │        │  ├── zoneinfo
   │  │  │     │     │        │  │  ├── Africa
   │  │  │     │     │        │  │  │  ├── Abidjan
   │  │  │     │     │        │  │  │  ├── Accra
   │  │  │     │     │        │  │  │  ├── Addis_Ababa
   │  │  │     │     │        │  │  │  ├── Algiers
   │  │  │     │     │        │  │  │  ├── Asmara
   │  │  │     │     │        │  │  │  ├── Asmera
   │  │  │     │     │        │  │  │  ├── Bamako
   │  │  │     │     │        │  │  │  ├── Bangui
   │  │  │     │     │        │  │  │  ├── Banjul
   │  │  │     │     │        │  │  │  ├── Bissau
   │  │  │     │     │        │  │  │  ├── Blantyre
   │  │  │     │     │        │  │  │  ├── Brazzaville
   │  │  │     │     │        │  │  │  ├── Bujumbura
   │  │  │     │     │        │  │  │  ├── Cairo
   │  │  │     │     │        │  │  │  ├── Casablanca
   │  │  │     │     │        │  │  │  ├── Ceuta
   │  │  │     │     │        │  │  │  ├── Conakry
   │  │  │     │     │        │  │  │  ├── Dakar
   │  │  │     │     │        │  │  │  ├── Dar_es_Salaam
   │  │  │     │     │        │  │  │  ├── Djibouti
   │  │  │     │     │        │  │  │  ├── Douala
   │  │  │     │     │        │  │  │  ├── El_Aaiun
   │  │  │     │     │        │  │  │  ├── Freetown
   │  │  │     │     │        │  │  │  ├── Gaborone
   │  │  │     │     │        │  │  │  ├── Harare
   │  │  │     │     │        │  │  │  ├── Johannesburg
   │  │  │     │     │        │  │  │  ├── Juba
   │  │  │     │     │        │  │  │  ├── Kampala
   │  │  │     │     │        │  │  │  ├── Khartoum
   │  │  │     │     │        │  │  │  ├── Kigali
   │  │  │     │     │        │  │  │  ├── Kinshasa
   │  │  │     │     │        │  │  │  ├── Lagos
   │  │  │     │     │        │  │  │  ├── Libreville
   │  │  │     │     │        │  │  │  ├── Lome
   │  │  │     │     │        │  │  │  ├── Luanda
   │  │  │     │     │        │  │  │  ├── Lubumbashi
   │  │  │     │     │        │  │  │  ├── Lusaka
   │  │  │     │     │        │  │  │  ├── Malabo
   │  │  │     │     │        │  │  │  ├── Maputo
   │  │  │     │     │        │  │  │  ├── Maseru
   │  │  │     │     │        │  │  │  ├── Mbabane
   │  │  │     │     │        │  │  │  ├── Mogadishu
   │  │  │     │     │        │  │  │  ├── Monrovia
   │  │  │     │     │        │  │  │  ├── Nairobi
   │  │  │     │     │        │  │  │  ├── Ndjamena
   │  │  │     │     │        │  │  │  ├── Niamey
   │  │  │     │     │        │  │  │  ├── Nouakchott
   │  │  │     │     │        │  │  │  ├── Ouagadougou
   │  │  │     │     │        │  │  │  ├── Porto-Novo
   │  │  │     │     │        │  │  │  ├── Sao_Tome
   │  │  │     │     │        │  │  │  ├── Timbuktu
   │  │  │     │     │        │  │  │  ├── Tripoli
   │  │  │     │     │        │  │  │  ├── Tunis
   │  │  │     │     │        │  │  │  ├── Windhoek
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── America
   │  │  │     │     │        │  │  │  ├── Adak
   │  │  │     │     │        │  │  │  ├── Anchorage
   │  │  │     │     │        │  │  │  ├── Anguilla
   │  │  │     │     │        │  │  │  ├── Antigua
   │  │  │     │     │        │  │  │  ├── Araguaina
   │  │  │     │     │        │  │  │  ├── Argentina
   │  │  │     │     │        │  │  │  │  ├── Buenos_Aires
   │  │  │     │     │        │  │  │  │  ├── Catamarca
   │  │  │     │     │        │  │  │  │  ├── ComodRivadavia
   │  │  │     │     │        │  │  │  │  ├── Cordoba
   │  │  │     │     │        │  │  │  │  ├── Jujuy
   │  │  │     │     │        │  │  │  │  ├── La_Rioja
   │  │  │     │     │        │  │  │  │  ├── Mendoza
   │  │  │     │     │        │  │  │  │  ├── Rio_Gallegos
   │  │  │     │     │        │  │  │  │  ├── Salta
   │  │  │     │     │        │  │  │  │  ├── San_Juan
   │  │  │     │     │        │  │  │  │  ├── San_Luis
   │  │  │     │     │        │  │  │  │  ├── Tucuman
   │  │  │     │     │        │  │  │  │  ├── Ushuaia
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── Aruba
   │  │  │     │     │        │  │  │  ├── Asuncion
   │  │  │     │     │        │  │  │  ├── Atikokan
   │  │  │     │     │        │  │  │  ├── Atka
   │  │  │     │     │        │  │  │  ├── Bahia
   │  │  │     │     │        │  │  │  ├── Bahia_Banderas
   │  │  │     │     │        │  │  │  ├── Barbados
   │  │  │     │     │        │  │  │  ├── Belem
   │  │  │     │     │        │  │  │  ├── Belize
   │  │  │     │     │        │  │  │  ├── Blanc-Sablon
   │  │  │     │     │        │  │  │  ├── Boa_Vista
   │  │  │     │     │        │  │  │  ├── Bogota
   │  │  │     │     │        │  │  │  ├── Boise
   │  │  │     │     │        │  │  │  ├── Buenos_Aires
   │  │  │     │     │        │  │  │  ├── Cambridge_Bay
   │  │  │     │     │        │  │  │  ├── Campo_Grande
   │  │  │     │     │        │  │  │  ├── Cancun
   │  │  │     │     │        │  │  │  ├── Caracas
   │  │  │     │     │        │  │  │  ├── Catamarca
   │  │  │     │     │        │  │  │  ├── Cayenne
   │  │  │     │     │        │  │  │  ├── Cayman
   │  │  │     │     │        │  │  │  ├── Chicago
   │  │  │     │     │        │  │  │  ├── Chihuahua
   │  │  │     │     │        │  │  │  ├── Ciudad_Juarez
   │  │  │     │     │        │  │  │  ├── Coral_Harbour
   │  │  │     │     │        │  │  │  ├── Cordoba
   │  │  │     │     │        │  │  │  ├── Costa_Rica
   │  │  │     │     │        │  │  │  ├── Coyhaique
   │  │  │     │     │        │  │  │  ├── Creston
   │  │  │     │     │        │  │  │  ├── Cuiaba
   │  │  │     │     │        │  │  │  ├── Curacao
   │  │  │     │     │        │  │  │  ├── Danmarkshavn
   │  │  │     │     │        │  │  │  ├── Dawson
   │  │  │     │     │        │  │  │  ├── Dawson_Creek
   │  │  │     │     │        │  │  │  ├── Denver
   │  │  │     │     │        │  │  │  ├── Detroit
   │  │  │     │     │        │  │  │  ├── Dominica
   │  │  │     │     │        │  │  │  ├── Edmonton
   │  │  │     │     │        │  │  │  ├── Eirunepe
   │  │  │     │     │        │  │  │  ├── El_Salvador
   │  │  │     │     │        │  │  │  ├── Ensenada
   │  │  │     │     │        │  │  │  ├── Fortaleza
   │  │  │     │     │        │  │  │  ├── Fort_Nelson
   │  │  │     │     │        │  │  │  ├── Fort_Wayne
   │  │  │     │     │        │  │  │  ├── Glace_Bay
   │  │  │     │     │        │  │  │  ├── Godthab
   │  │  │     │     │        │  │  │  ├── Goose_Bay
   │  │  │     │     │        │  │  │  ├── Grand_Turk
   │  │  │     │     │        │  │  │  ├── Grenada
   │  │  │     │     │        │  │  │  ├── Guadeloupe
   │  │  │     │     │        │  │  │  ├── Guatemala
   │  │  │     │     │        │  │  │  ├── Guayaquil
   │  │  │     │     │        │  │  │  ├── Guyana
   │  │  │     │     │        │  │  │  ├── Halifax
   │  │  │     │     │        │  │  │  ├── Havana
   │  │  │     │     │        │  │  │  ├── Hermosillo
   │  │  │     │     │        │  │  │  ├── Indiana
   │  │  │     │     │        │  │  │  │  ├── Indianapolis
   │  │  │     │     │        │  │  │  │  ├── Knox
   │  │  │     │     │        │  │  │  │  ├── Marengo
   │  │  │     │     │        │  │  │  │  ├── Petersburg
   │  │  │     │     │        │  │  │  │  ├── Tell_City
   │  │  │     │     │        │  │  │  │  ├── Vevay
   │  │  │     │     │        │  │  │  │  ├── Vincennes
   │  │  │     │     │        │  │  │  │  ├── Winamac
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── Indianapolis
   │  │  │     │     │        │  │  │  ├── Inuvik
   │  │  │     │     │        │  │  │  ├── Iqaluit
   │  │  │     │     │        │  │  │  ├── Jamaica
   │  │  │     │     │        │  │  │  ├── Jujuy
   │  │  │     │     │        │  │  │  ├── Juneau
   │  │  │     │     │        │  │  │  ├── Kentucky
   │  │  │     │     │        │  │  │  │  ├── Louisville
   │  │  │     │     │        │  │  │  │  ├── Monticello
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── Knox_IN
   │  │  │     │     │        │  │  │  ├── Kralendijk
   │  │  │     │     │        │  │  │  ├── La_Paz
   │  │  │     │     │        │  │  │  ├── Lima
   │  │  │     │     │        │  │  │  ├── Los_Angeles
   │  │  │     │     │        │  │  │  ├── Louisville
   │  │  │     │     │        │  │  │  ├── Lower_Princes
   │  │  │     │     │        │  │  │  ├── Maceio
   │  │  │     │     │        │  │  │  ├── Managua
   │  │  │     │     │        │  │  │  ├── Manaus
   │  │  │     │     │        │  │  │  ├── Marigot
   │  │  │     │     │        │  │  │  ├── Martinique
   │  │  │     │     │        │  │  │  ├── Matamoros
   │  │  │     │     │        │  │  │  ├── Mazatlan
   │  │  │     │     │        │  │  │  ├── Mendoza
   │  │  │     │     │        │  │  │  ├── Menominee
   │  │  │     │     │        │  │  │  ├── Merida
   │  │  │     │     │        │  │  │  ├── Metlakatla
   │  │  │     │     │        │  │  │  ├── Mexico_City
   │  │  │     │     │        │  │  │  ├── Miquelon
   │  │  │     │     │        │  │  │  ├── Moncton
   │  │  │     │     │        │  │  │  ├── Monterrey
   │  │  │     │     │        │  │  │  ├── Montevideo
   │  │  │     │     │        │  │  │  ├── Montreal
   │  │  │     │     │        │  │  │  ├── Montserrat
   │  │  │     │     │        │  │  │  ├── Nassau
   │  │  │     │     │        │  │  │  ├── New_York
   │  │  │     │     │        │  │  │  ├── Nipigon
   │  │  │     │     │        │  │  │  ├── Nome
   │  │  │     │     │        │  │  │  ├── Noronha
   │  │  │     │     │        │  │  │  ├── North_Dakota
   │  │  │     │     │        │  │  │  │  ├── Beulah
   │  │  │     │     │        │  │  │  │  ├── Center
   │  │  │     │     │        │  │  │  │  ├── New_Salem
   │  │  │     │     │        │  │  │  │  └── __init__.py
   │  │  │     │     │        │  │  │  ├── Nuuk
   │  │  │     │     │        │  │  │  ├── Ojinaga
   │  │  │     │     │        │  │  │  ├── Panama
   │  │  │     │     │        │  │  │  ├── Pangnirtung
   │  │  │     │     │        │  │  │  ├── Paramaribo
   │  │  │     │     │        │  │  │  ├── Phoenix
   │  │  │     │     │        │  │  │  ├── Port-au-Prince
   │  │  │     │     │        │  │  │  ├── Porto_Acre
   │  │  │     │     │        │  │  │  ├── Porto_Velho
   │  │  │     │     │        │  │  │  ├── Port_of_Spain
   │  │  │     │     │        │  │  │  ├── Puerto_Rico
   │  │  │     │     │        │  │  │  ├── Punta_Arenas
   │  │  │     │     │        │  │  │  ├── Rainy_River
   │  │  │     │     │        │  │  │  ├── Rankin_Inlet
   │  │  │     │     │        │  │  │  ├── Recife
   │  │  │     │     │        │  │  │  ├── Regina
   │  │  │     │     │        │  │  │  ├── Resolute
   │  │  │     │     │        │  │  │  ├── Rio_Branco
   │  │  │     │     │        │  │  │  ├── Rosario
   │  │  │     │     │        │  │  │  ├── Santarem
   │  │  │     │     │        │  │  │  ├── Santa_Isabel
   │  │  │     │     │        │  │  │  ├── Santiago
   │  │  │     │     │        │  │  │  ├── Santo_Domingo
   │  │  │     │     │        │  │  │  ├── Sao_Paulo
   │  │  │     │     │        │  │  │  ├── Scoresbysund
   │  │  │     │     │        │  │  │  ├── Shiprock
   │  │  │     │     │        │  │  │  ├── Sitka
   │  │  │     │     │        │  │  │  ├── St_Barthelemy
   │  │  │     │     │        │  │  │  ├── St_Johns
   │  │  │     │     │        │  │  │  ├── St_Kitts
   │  │  │     │     │        │  │  │  ├── St_Lucia
   │  │  │     │     │        │  │  │  ├── St_Thomas
   │  │  │     │     │        │  │  │  ├── St_Vincent
   │  │  │     │     │        │  │  │  ├── Swift_Current
   │  │  │     │     │        │  │  │  ├── Tegucigalpa
   │  │  │     │     │        │  │  │  ├── Thule
   │  │  │     │     │        │  │  │  ├── Thunder_Bay
   │  │  │     │     │        │  │  │  ├── Tijuana
   │  │  │     │     │        │  │  │  ├── Toronto
   │  │  │     │     │        │  │  │  ├── Tortola
   │  │  │     │     │        │  │  │  ├── Vancouver
   │  │  │     │     │        │  │  │  ├── Virgin
   │  │  │     │     │        │  │  │  ├── Whitehorse
   │  │  │     │     │        │  │  │  ├── Winnipeg
   │  │  │     │     │        │  │  │  ├── Yakutat
   │  │  │     │     │        │  │  │  ├── Yellowknife
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Antarctica
   │  │  │     │     │        │  │  │  ├── Casey
   │  │  │     │     │        │  │  │  ├── Davis
   │  │  │     │     │        │  │  │  ├── DumontDUrville
   │  │  │     │     │        │  │  │  ├── Macquarie
   │  │  │     │     │        │  │  │  ├── Mawson
   │  │  │     │     │        │  │  │  ├── McMurdo
   │  │  │     │     │        │  │  │  ├── Palmer
   │  │  │     │     │        │  │  │  ├── Rothera
   │  │  │     │     │        │  │  │  ├── South_Pole
   │  │  │     │     │        │  │  │  ├── Syowa
   │  │  │     │     │        │  │  │  ├── Troll
   │  │  │     │     │        │  │  │  ├── Vostok
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Arctic
   │  │  │     │     │        │  │  │  ├── Longyearbyen
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Asia
   │  │  │     │     │        │  │  │  ├── Aden
   │  │  │     │     │        │  │  │  ├── Almaty
   │  │  │     │     │        │  │  │  ├── Amman
   │  │  │     │     │        │  │  │  ├── Anadyr
   │  │  │     │     │        │  │  │  ├── Aqtau
   │  │  │     │     │        │  │  │  ├── Aqtobe
   │  │  │     │     │        │  │  │  ├── Ashgabat
   │  │  │     │     │        │  │  │  ├── Ashkhabad
   │  │  │     │     │        │  │  │  ├── Atyrau
   │  │  │     │     │        │  │  │  ├── Baghdad
   │  │  │     │     │        │  │  │  ├── Bahrain
   │  │  │     │     │        │  │  │  ├── Baku
   │  │  │     │     │        │  │  │  ├── Bangkok
   │  │  │     │     │        │  │  │  ├── Barnaul
   │  │  │     │     │        │  │  │  ├── Beirut
   │  │  │     │     │        │  │  │  ├── Bishkek
   │  │  │     │     │        │  │  │  ├── Brunei
   │  │  │     │     │        │  │  │  ├── Calcutta
   │  │  │     │     │        │  │  │  ├── Chita
   │  │  │     │     │        │  │  │  ├── Choibalsan
   │  │  │     │     │        │  │  │  ├── Chongqing
   │  │  │     │     │        │  │  │  ├── Chungking
   │  │  │     │     │        │  │  │  ├── Colombo
   │  │  │     │     │        │  │  │  ├── Dacca
   │  │  │     │     │        │  │  │  ├── Damascus
   │  │  │     │     │        │  │  │  ├── Dhaka
   │  │  │     │     │        │  │  │  ├── Dili
   │  │  │     │     │        │  │  │  ├── Dubai
   │  │  │     │     │        │  │  │  ├── Dushanbe
   │  │  │     │     │        │  │  │  ├── Famagusta
   │  │  │     │     │        │  │  │  ├── Gaza
   │  │  │     │     │        │  │  │  ├── Harbin
   │  │  │     │     │        │  │  │  ├── Hebron
   │  │  │     │     │        │  │  │  ├── Hong_Kong
   │  │  │     │     │        │  │  │  ├── Hovd
   │  │  │     │     │        │  │  │  ├── Ho_Chi_Minh
   │  │  │     │     │        │  │  │  ├── Irkutsk
   │  │  │     │     │        │  │  │  ├── Istanbul
   │  │  │     │     │        │  │  │  ├── Jakarta
   │  │  │     │     │        │  │  │  ├── Jayapura
   │  │  │     │     │        │  │  │  ├── Jerusalem
   │  │  │     │     │        │  │  │  ├── Kabul
   │  │  │     │     │        │  │  │  ├── Kamchatka
   │  │  │     │     │        │  │  │  ├── Karachi
   │  │  │     │     │        │  │  │  ├── Kashgar
   │  │  │     │     │        │  │  │  ├── Kathmandu
   │  │  │     │     │        │  │  │  ├── Katmandu
   │  │  │     │     │        │  │  │  ├── Khandyga
   │  │  │     │     │        │  │  │  ├── Kolkata
   │  │  │     │     │        │  │  │  ├── Krasnoyarsk
   │  │  │     │     │        │  │  │  ├── Kuala_Lumpur
   │  │  │     │     │        │  │  │  ├── Kuching
   │  │  │     │     │        │  │  │  ├── Kuwait
   │  │  │     │     │        │  │  │  ├── Macao
   │  │  │     │     │        │  │  │  ├── Macau
   │  │  │     │     │        │  │  │  ├── Magadan
   │  │  │     │     │        │  │  │  ├── Makassar
   │  │  │     │     │        │  │  │  ├── Manila
   │  │  │     │     │        │  │  │  ├── Muscat
   │  │  │     │     │        │  │  │  ├── Nicosia
   │  │  │     │     │        │  │  │  ├── Novokuznetsk
   │  │  │     │     │        │  │  │  ├── Novosibirsk
   │  │  │     │     │        │  │  │  ├── Omsk
   │  │  │     │     │        │  │  │  ├── Oral
   │  │  │     │     │        │  │  │  ├── Phnom_Penh
   │  │  │     │     │        │  │  │  ├── Pontianak
   │  │  │     │     │        │  │  │  ├── Pyongyang
   │  │  │     │     │        │  │  │  ├── Qatar
   │  │  │     │     │        │  │  │  ├── Qostanay
   │  │  │     │     │        │  │  │  ├── Qyzylorda
   │  │  │     │     │        │  │  │  ├── Rangoon
   │  │  │     │     │        │  │  │  ├── Riyadh
   │  │  │     │     │        │  │  │  ├── Saigon
   │  │  │     │     │        │  │  │  ├── Sakhalin
   │  │  │     │     │        │  │  │  ├── Samarkand
   │  │  │     │     │        │  │  │  ├── Seoul
   │  │  │     │     │        │  │  │  ├── Shanghai
   │  │  │     │     │        │  │  │  ├── Singapore
   │  │  │     │     │        │  │  │  ├── Srednekolymsk
   │  │  │     │     │        │  │  │  ├── Taipei
   │  │  │     │     │        │  │  │  ├── Tashkent
   │  │  │     │     │        │  │  │  ├── Tbilisi
   │  │  │     │     │        │  │  │  ├── Tehran
   │  │  │     │     │        │  │  │  ├── Tel_Aviv
   │  │  │     │     │        │  │  │  ├── Thimbu
   │  │  │     │     │        │  │  │  ├── Thimphu
   │  │  │     │     │        │  │  │  ├── Tokyo
   │  │  │     │     │        │  │  │  ├── Tomsk
   │  │  │     │     │        │  │  │  ├── Ujung_Pandang
   │  │  │     │     │        │  │  │  ├── Ulaanbaatar
   │  │  │     │     │        │  │  │  ├── Ulan_Bator
   │  │  │     │     │        │  │  │  ├── Urumqi
   │  │  │     │     │        │  │  │  ├── Ust-Nera
   │  │  │     │     │        │  │  │  ├── Vientiane
   │  │  │     │     │        │  │  │  ├── Vladivostok
   │  │  │     │     │        │  │  │  ├── Yakutsk
   │  │  │     │     │        │  │  │  ├── Yangon
   │  │  │     │     │        │  │  │  ├── Yekaterinburg
   │  │  │     │     │        │  │  │  ├── Yerevan
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Atlantic
   │  │  │     │     │        │  │  │  ├── Azores
   │  │  │     │     │        │  │  │  ├── Bermuda
   │  │  │     │     │        │  │  │  ├── Canary
   │  │  │     │     │        │  │  │  ├── Cape_Verde
   │  │  │     │     │        │  │  │  ├── Faeroe
   │  │  │     │     │        │  │  │  ├── Faroe
   │  │  │     │     │        │  │  │  ├── Jan_Mayen
   │  │  │     │     │        │  │  │  ├── Madeira
   │  │  │     │     │        │  │  │  ├── Reykjavik
   │  │  │     │     │        │  │  │  ├── South_Georgia
   │  │  │     │     │        │  │  │  ├── Stanley
   │  │  │     │     │        │  │  │  ├── St_Helena
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Australia
   │  │  │     │     │        │  │  │  ├── ACT
   │  │  │     │     │        │  │  │  ├── Adelaide
   │  │  │     │     │        │  │  │  ├── Brisbane
   │  │  │     │     │        │  │  │  ├── Broken_Hill
   │  │  │     │     │        │  │  │  ├── Canberra
   │  │  │     │     │        │  │  │  ├── Currie
   │  │  │     │     │        │  │  │  ├── Darwin
   │  │  │     │     │        │  │  │  ├── Eucla
   │  │  │     │     │        │  │  │  ├── Hobart
   │  │  │     │     │        │  │  │  ├── LHI
   │  │  │     │     │        │  │  │  ├── Lindeman
   │  │  │     │     │        │  │  │  ├── Lord_Howe
   │  │  │     │     │        │  │  │  ├── Melbourne
   │  │  │     │     │        │  │  │  ├── North
   │  │  │     │     │        │  │  │  ├── NSW
   │  │  │     │     │        │  │  │  ├── Perth
   │  │  │     │     │        │  │  │  ├── Queensland
   │  │  │     │     │        │  │  │  ├── South
   │  │  │     │     │        │  │  │  ├── Sydney
   │  │  │     │     │        │  │  │  ├── Tasmania
   │  │  │     │     │        │  │  │  ├── Victoria
   │  │  │     │     │        │  │  │  ├── West
   │  │  │     │     │        │  │  │  ├── Yancowinna
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Brazil
   │  │  │     │     │        │  │  │  ├── Acre
   │  │  │     │     │        │  │  │  ├── DeNoronha
   │  │  │     │     │        │  │  │  ├── East
   │  │  │     │     │        │  │  │  ├── West
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Canada
   │  │  │     │     │        │  │  │  ├── Atlantic
   │  │  │     │     │        │  │  │  ├── Central
   │  │  │     │     │        │  │  │  ├── Eastern
   │  │  │     │     │        │  │  │  ├── Mountain
   │  │  │     │     │        │  │  │  ├── Newfoundland
   │  │  │     │     │        │  │  │  ├── Pacific
   │  │  │     │     │        │  │  │  ├── Saskatchewan
   │  │  │     │     │        │  │  │  ├── Yukon
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── CET
   │  │  │     │     │        │  │  ├── Chile
   │  │  │     │     │        │  │  │  ├── Continental
   │  │  │     │     │        │  │  │  ├── EasterIsland
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── CST6CDT
   │  │  │     │     │        │  │  ├── Cuba
   │  │  │     │     │        │  │  ├── EET
   │  │  │     │     │        │  │  ├── Egypt
   │  │  │     │     │        │  │  ├── Eire
   │  │  │     │     │        │  │  ├── EST
   │  │  │     │     │        │  │  ├── EST5EDT
   │  │  │     │     │        │  │  ├── Etc
   │  │  │     │     │        │  │  │  ├── GMT
   │  │  │     │     │        │  │  │  ├── GMT+0
   │  │  │     │     │        │  │  │  ├── GMT+1
   │  │  │     │     │        │  │  │  ├── GMT+10
   │  │  │     │     │        │  │  │  ├── GMT+11
   │  │  │     │     │        │  │  │  ├── GMT+12
   │  │  │     │     │        │  │  │  ├── GMT+2
   │  │  │     │     │        │  │  │  ├── GMT+3
   │  │  │     │     │        │  │  │  ├── GMT+4
   │  │  │     │     │        │  │  │  ├── GMT+5
   │  │  │     │     │        │  │  │  ├── GMT+6
   │  │  │     │     │        │  │  │  ├── GMT+7
   │  │  │     │     │        │  │  │  ├── GMT+8
   │  │  │     │     │        │  │  │  ├── GMT+9
   │  │  │     │     │        │  │  │  ├── GMT-0
   │  │  │     │     │        │  │  │  ├── GMT-1
   │  │  │     │     │        │  │  │  ├── GMT-10
   │  │  │     │     │        │  │  │  ├── GMT-11
   │  │  │     │     │        │  │  │  ├── GMT-12
   │  │  │     │     │        │  │  │  ├── GMT-13
   │  │  │     │     │        │  │  │  ├── GMT-14
   │  │  │     │     │        │  │  │  ├── GMT-2
   │  │  │     │     │        │  │  │  ├── GMT-3
   │  │  │     │     │        │  │  │  ├── GMT-4
   │  │  │     │     │        │  │  │  ├── GMT-5
   │  │  │     │     │        │  │  │  ├── GMT-6
   │  │  │     │     │        │  │  │  ├── GMT-7
   │  │  │     │     │        │  │  │  ├── GMT-8
   │  │  │     │     │        │  │  │  ├── GMT-9
   │  │  │     │     │        │  │  │  ├── GMT0
   │  │  │     │     │        │  │  │  ├── Greenwich
   │  │  │     │     │        │  │  │  ├── UCT
   │  │  │     │     │        │  │  │  ├── Universal
   │  │  │     │     │        │  │  │  ├── UTC
   │  │  │     │     │        │  │  │  ├── Zulu
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Europe
   │  │  │     │     │        │  │  │  ├── Amsterdam
   │  │  │     │     │        │  │  │  ├── Andorra
   │  │  │     │     │        │  │  │  ├── Astrakhan
   │  │  │     │     │        │  │  │  ├── Athens
   │  │  │     │     │        │  │  │  ├── Belfast
   │  │  │     │     │        │  │  │  ├── Belgrade
   │  │  │     │     │        │  │  │  ├── Berlin
   │  │  │     │     │        │  │  │  ├── Bratislava
   │  │  │     │     │        │  │  │  ├── Brussels
   │  │  │     │     │        │  │  │  ├── Bucharest
   │  │  │     │     │        │  │  │  ├── Budapest
   │  │  │     │     │        │  │  │  ├── Busingen
   │  │  │     │     │        │  │  │  ├── Chisinau
   │  │  │     │     │        │  │  │  ├── Copenhagen
   │  │  │     │     │        │  │  │  ├── Dublin
   │  │  │     │     │        │  │  │  ├── Gibraltar
   │  │  │     │     │        │  │  │  ├── Guernsey
   │  │  │     │     │        │  │  │  ├── Helsinki
   │  │  │     │     │        │  │  │  ├── Isle_of_Man
   │  │  │     │     │        │  │  │  ├── Istanbul
   │  │  │     │     │        │  │  │  ├── Jersey
   │  │  │     │     │        │  │  │  ├── Kaliningrad
   │  │  │     │     │        │  │  │  ├── Kiev
   │  │  │     │     │        │  │  │  ├── Kirov
   │  │  │     │     │        │  │  │  ├── Kyiv
   │  │  │     │     │        │  │  │  ├── Lisbon
   │  │  │     │     │        │  │  │  ├── Ljubljana
   │  │  │     │     │        │  │  │  ├── London
   │  │  │     │     │        │  │  │  ├── Luxembourg
   │  │  │     │     │        │  │  │  ├── Madrid
   │  │  │     │     │        │  │  │  ├── Malta
   │  │  │     │     │        │  │  │  ├── Mariehamn
   │  │  │     │     │        │  │  │  ├── Minsk
   │  │  │     │     │        │  │  │  ├── Monaco
   │  │  │     │     │        │  │  │  ├── Moscow
   │  │  │     │     │        │  │  │  ├── Nicosia
   │  │  │     │     │        │  │  │  ├── Oslo
   │  │  │     │     │        │  │  │  ├── Paris
   │  │  │     │     │        │  │  │  ├── Podgorica
   │  │  │     │     │        │  │  │  ├── Prague
   │  │  │     │     │        │  │  │  ├── Riga
   │  │  │     │     │        │  │  │  ├── Rome
   │  │  │     │     │        │  │  │  ├── Samara
   │  │  │     │     │        │  │  │  ├── San_Marino
   │  │  │     │     │        │  │  │  ├── Sarajevo
   │  │  │     │     │        │  │  │  ├── Saratov
   │  │  │     │     │        │  │  │  ├── Simferopol
   │  │  │     │     │        │  │  │  ├── Skopje
   │  │  │     │     │        │  │  │  ├── Sofia
   │  │  │     │     │        │  │  │  ├── Stockholm
   │  │  │     │     │        │  │  │  ├── Tallinn
   │  │  │     │     │        │  │  │  ├── Tirane
   │  │  │     │     │        │  │  │  ├── Tiraspol
   │  │  │     │     │        │  │  │  ├── Ulyanovsk
   │  │  │     │     │        │  │  │  ├── Uzhgorod
   │  │  │     │     │        │  │  │  ├── Vaduz
   │  │  │     │     │        │  │  │  ├── Vatican
   │  │  │     │     │        │  │  │  ├── Vienna
   │  │  │     │     │        │  │  │  ├── Vilnius
   │  │  │     │     │        │  │  │  ├── Volgograd
   │  │  │     │     │        │  │  │  ├── Warsaw
   │  │  │     │     │        │  │  │  ├── Zagreb
   │  │  │     │     │        │  │  │  ├── Zaporozhye
   │  │  │     │     │        │  │  │  ├── Zurich
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Factory
   │  │  │     │     │        │  │  ├── GB
   │  │  │     │     │        │  │  ├── GB-Eire
   │  │  │     │     │        │  │  ├── GMT
   │  │  │     │     │        │  │  ├── GMT+0
   │  │  │     │     │        │  │  ├── GMT-0
   │  │  │     │     │        │  │  ├── GMT0
   │  │  │     │     │        │  │  ├── Greenwich
   │  │  │     │     │        │  │  ├── Hongkong
   │  │  │     │     │        │  │  ├── HST
   │  │  │     │     │        │  │  ├── Iceland
   │  │  │     │     │        │  │  ├── Indian
   │  │  │     │     │        │  │  │  ├── Antananarivo
   │  │  │     │     │        │  │  │  ├── Chagos
   │  │  │     │     │        │  │  │  ├── Christmas
   │  │  │     │     │        │  │  │  ├── Cocos
   │  │  │     │     │        │  │  │  ├── Comoro
   │  │  │     │     │        │  │  │  ├── Kerguelen
   │  │  │     │     │        │  │  │  ├── Mahe
   │  │  │     │     │        │  │  │  ├── Maldives
   │  │  │     │     │        │  │  │  ├── Mauritius
   │  │  │     │     │        │  │  │  ├── Mayotte
   │  │  │     │     │        │  │  │  ├── Reunion
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Iran
   │  │  │     │     │        │  │  ├── iso3166.tab
   │  │  │     │     │        │  │  ├── Israel
   │  │  │     │     │        │  │  ├── Jamaica
   │  │  │     │     │        │  │  ├── Japan
   │  │  │     │     │        │  │  ├── Kwajalein
   │  │  │     │     │        │  │  ├── leapseconds
   │  │  │     │     │        │  │  ├── Libya
   │  │  │     │     │        │  │  ├── MET
   │  │  │     │     │        │  │  ├── Mexico
   │  │  │     │     │        │  │  │  ├── BajaNorte
   │  │  │     │     │        │  │  │  ├── BajaSur
   │  │  │     │     │        │  │  │  ├── General
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── MST
   │  │  │     │     │        │  │  ├── MST7MDT
   │  │  │     │     │        │  │  ├── Navajo
   │  │  │     │     │        │  │  ├── NZ
   │  │  │     │     │        │  │  ├── NZ-CHAT
   │  │  │     │     │        │  │  ├── Pacific
   │  │  │     │     │        │  │  │  ├── Apia
   │  │  │     │     │        │  │  │  ├── Auckland
   │  │  │     │     │        │  │  │  ├── Bougainville
   │  │  │     │     │        │  │  │  ├── Chatham
   │  │  │     │     │        │  │  │  ├── Chuuk
   │  │  │     │     │        │  │  │  ├── Easter
   │  │  │     │     │        │  │  │  ├── Efate
   │  │  │     │     │        │  │  │  ├── Enderbury
   │  │  │     │     │        │  │  │  ├── Fakaofo
   │  │  │     │     │        │  │  │  ├── Fiji
   │  │  │     │     │        │  │  │  ├── Funafuti
   │  │  │     │     │        │  │  │  ├── Galapagos
   │  │  │     │     │        │  │  │  ├── Gambier
   │  │  │     │     │        │  │  │  ├── Guadalcanal
   │  │  │     │     │        │  │  │  ├── Guam
   │  │  │     │     │        │  │  │  ├── Honolulu
   │  │  │     │     │        │  │  │  ├── Johnston
   │  │  │     │     │        │  │  │  ├── Kanton
   │  │  │     │     │        │  │  │  ├── Kiritimati
   │  │  │     │     │        │  │  │  ├── Kosrae
   │  │  │     │     │        │  │  │  ├── Kwajalein
   │  │  │     │     │        │  │  │  ├── Majuro
   │  │  │     │     │        │  │  │  ├── Marquesas
   │  │  │     │     │        │  │  │  ├── Midway
   │  │  │     │     │        │  │  │  ├── Nauru
   │  │  │     │     │        │  │  │  ├── Niue
   │  │  │     │     │        │  │  │  ├── Norfolk
   │  │  │     │     │        │  │  │  ├── Noumea
   │  │  │     │     │        │  │  │  ├── Pago_Pago
   │  │  │     │     │        │  │  │  ├── Palau
   │  │  │     │     │        │  │  │  ├── Pitcairn
   │  │  │     │     │        │  │  │  ├── Pohnpei
   │  │  │     │     │        │  │  │  ├── Ponape
   │  │  │     │     │        │  │  │  ├── Port_Moresby
   │  │  │     │     │        │  │  │  ├── Rarotonga
   │  │  │     │     │        │  │  │  ├── Saipan
   │  │  │     │     │        │  │  │  ├── Samoa
   │  │  │     │     │        │  │  │  ├── Tahiti
   │  │  │     │     │        │  │  │  ├── Tarawa
   │  │  │     │     │        │  │  │  ├── Tongatapu
   │  │  │     │     │        │  │  │  ├── Truk
   │  │  │     │     │        │  │  │  ├── Wake
   │  │  │     │     │        │  │  │  ├── Wallis
   │  │  │     │     │        │  │  │  ├── Yap
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── Poland
   │  │  │     │     │        │  │  ├── Portugal
   │  │  │     │     │        │  │  ├── PRC
   │  │  │     │     │        │  │  ├── PST8PDT
   │  │  │     │     │        │  │  ├── ROC
   │  │  │     │     │        │  │  ├── ROK
   │  │  │     │     │        │  │  ├── Singapore
   │  │  │     │     │        │  │  ├── Turkey
   │  │  │     │     │        │  │  ├── tzdata.zi
   │  │  │     │     │        │  │  ├── UCT
   │  │  │     │     │        │  │  ├── Universal
   │  │  │     │     │        │  │  ├── US
   │  │  │     │     │        │  │  │  ├── Alaska
   │  │  │     │     │        │  │  │  ├── Aleutian
   │  │  │     │     │        │  │  │  ├── Arizona
   │  │  │     │     │        │  │  │  ├── Central
   │  │  │     │     │        │  │  │  ├── East-Indiana
   │  │  │     │     │        │  │  │  ├── Eastern
   │  │  │     │     │        │  │  │  ├── Hawaii
   │  │  │     │     │        │  │  │  ├── Indiana-Starke
   │  │  │     │     │        │  │  │  ├── Michigan
   │  │  │     │     │        │  │  │  ├── Mountain
   │  │  │     │     │        │  │  │  ├── Pacific
   │  │  │     │     │        │  │  │  ├── Samoa
   │  │  │     │     │        │  │  │  └── __init__.py
   │  │  │     │     │        │  │  ├── UTC
   │  │  │     │     │        │  │  ├── W-SU
   │  │  │     │     │        │  │  ├── WET
   │  │  │     │     │        │  │  ├── zone.tab
   │  │  │     │     │        │  │  ├── zone1970.tab
   │  │  │     │     │        │  │  ├── zonenow.tab
   │  │  │     │     │        │  │  ├── Zulu
   │  │  │     │     │        │  │  └── __init__.py
   │  │  │     │     │        │  ├── zones
   │  │  │     │     │        │  └── __init__.py
   │  │  │     │     │       └── tzdata-2025.2.dist-info
   │  │  │     │     │          ├── INSTALLER
   │  │  │     │     │          ├── licenses
   │  │  │     │     │           │  ├── LICENSE
   │  │  │     │     │           │  └── licenses
   │  │  │     │     │           │    └── LICENSE_APACHE
   │  │  │     │     │          ├── METADATA
   │  │  │     │     │          ├── RECORD
   │  │  │     │     │          ├── top_level.txt
   │  │  │     │     │          └── WHEEL
   │  │  │     │    ├── lib64
   │  │  │     │    └── pyvenv.cfg
   │  │  │    ├── Complete_Co_Analysis
   │  │  │     │  ├── banks.csv
   │  │  │     │  ├── cafes.csv
   │  │  │     │  ├── education.csv
   │  │  │     │  ├── health.csv
   │  │  │     │  ├── other.csv
   │  │  │     │  └── temples.csv
   │  │  │    ├── Complete_Co_Analysis.zip
   │  │  │    ├── inco_poi.json
   │  │  │    ├── inside_poi_temple_bank_gym_library.json
   │  │  │    ├── in_hos_colle_school.json
   │  │  │    ├── other_poi.json
   │  │  │    ├── pois
   │  │  │     │  └── csv
   │  │  │     │    ├── by_category
   │  │  │     │     │  ├── banks.csv
   │  │  │     │     │  ├── banks.json
   │  │  │     │     │  ├── banks_all_data.csv
   │  │  │     │     │  ├── cafes.csv
   │  │  │     │     │  ├── cafes.json
   │  │  │     │     │  ├── cafes_all_data.csv
   │  │  │     │     │  ├── education.csv
   │  │  │     │     │  ├── education.json
   │  │  │     │     │  ├── education_all_data.csv
   │  │  │     │     │  ├── health.csv
   │  │  │     │     │  ├── health.json
   │  │  │     │     │  ├── health_all_data.csv
   │  │  │     │     │  ├── other.csv
   │  │  │     │     │  ├── other.json
   │  │  │     │     │  ├── other_all_data.csv
   │  │  │     │     │  ├── temples.csv
   │  │  │     │     │  ├── temples.json
   │  │  │     │     │  └── temples_all_data.csv
   │  │  │     │    ├── pois_category_summary.csv
   │  │  │     │    ├── pois_compact_summary.csv
   │  │  │     │    ├── pois_flattened_all_fields.csv
   │  │  │     │    └── pois_missing_category_rule.csv
   │  │  │    ├── scripts
   │  │  │     │  ├── csv_to_geojson.py
   │  │  │     │  ├── generate_distributions.py
   │  │  │     │  └── merge_generated.py
   │  │  │    ├── split_by_category.py
   │  │  │    └── unique_categories.txt
   │  │  ├── filter_columns.py
   │  │  ├── ktm_cafe.db
   │  │  ├── ktm_pois.db
   │  │  ├── ktm_pois.db-journal
   │  │  ├── ktm_restaurants.db
   │  │  ├── ktm_restaurants2.db
   │  │  ├── master.ipynb
   │  │  ├── master.py
   │  │  ├── Roadway.geojson
   │  │  ├── Roadway.graph.pkl
   │  │  ├── Roadway.graph_osmnx.pkl
   │  │  ├── Roadway.graph_osmnx_valley.pkl
   │  │  ├── Roadway.roadtypes.pkl
   │  │  ├── roadway_preview.html
   │  │  ├── road_graph_cache.pkl
   │  │  ├── road_graph_cache_osmnx.pkl
   │  │  ├── road_graph_cache_osmnx_osmnx.pkl
   │  │  ├── road_graph_cache_osmnx_osmnx_valley.pkl
   │  │  ├── score_entries.py
   │  │  ├── test.py
   │  │  └── which_config_used.py
   │  ├── mod_spatialite-5.1.0-win-amd64
   │  │  ├── libcrypto-3-x64.dll
   │  │  ├── libcurl-4.dll
   │  │  ├── libexpat-1.dll
   │  │  ├── libfreexl-1.dll
   │  │  ├── libgcc_s_seh-1.dll
   │  │  ├── libgeos.dll
   │  │  ├── libgeos_c.dll
   │  │  ├── libiconv-2.dll
   │  │  ├── libjpeg-62.dll
   │  │  ├── liblzma-5.dll
   │  │  ├── libminizip-1.dll
   │  │  ├── libproj_9_2.dll
   │  │  ├── libreadline8.dll
   │  │  ├── librttopo-1.dll
   │  │  ├── libsharpyuv-0.dll
   │  │  ├── libsqlite3-0.dll
   │  │  ├── libssl-3-x64.dll
   │  │  ├── libstdc++-6.dll
   │  │  ├── libtermcap-0.dll
   │  │  ├── libtiff-6.dll
   │  │  ├── libwebp-7.dll
   │  │  ├── libwinpthread-1.dll
   │  │  ├── libxml2.dll
   │  │  ├── libzstd.dll
   │  │  ├── mod_spatialite.dll
   │  │  ├── proj.db
   │  │  ├── sqlite3.exe
   │  │  └── zlib1.dll
   │  ├── notebooks
   │  │  ├── poi_density_heatmap.ipynb
   │  │  ├── roadway_visualization.ipynb
   │  │  ├── spatialite_migration.ipynb
   │  │  └── train_xgb.ipynb
   │  ├── pois.json
   │  ├── README.md
   │  ├── requirements.txt
   │  ├── RoadNetwork_Export.geojson
   │  ├── road_network_interactive.html
   │  ├── road_network_visualization.png
   │  ├── scripts
   │  │  ├── export_cafe_poi_paths.py
   │  │  ├── inspect_model.py
   │  │  ├── inspect_model_pickle.py
   │  │  ├── inspect_stream.py
   │  │  ├── pois_inspect.py
   │  │  ├── pois_inspect_README.md
   │  │  ├── scratch_node_type.py
   │  │  ├── scratch_test.py
   │  │  ├── scratch_test2.py
   │  │  ├── scratch_test3.py
   │  │  ├── scratch_test4.py
   │  │  ├── scratch_test5.py
   │  │  ├── scratch_test6.py
   │  │  ├── scratch_test7.py
   │  │  ├── test_osmnx_integration.py
   │  │  ├── test_pois.py
   │  │  ├── test_pois_direct.py
   │  │  ├── test_predict.py
   │  │  ├── verify_fixes.py
   │  │  ├── visualize_road_network.py
   │  │  └── visualize_road_network_folium.py
   │  ├── sitex_geospatial.db
   │  ├── tests
   │  │  ├── test_analysis.py
   │  │  ├── test_api.py
   │  │  ├── test_gnn_and_fixes.py
   │  │  ├── test_pois_decay.py
   │  │  ├── test_pois_inspect.py
   │  │  └── __init__.py
   │  └── __init__.py
  ├── Docs
   │  ├── context.txt
   │  ├── features.txt
   │  ├── implementation_plan.md
   │  ├── SiteX_Features.docx.pdf
   │  ├── sitex_final_semester_plan_v2.html
   │  ├── SiteX_Project_Context.docx.pdf
   │  ├── sitex_team_research_topics.html
   │  ├── SPATIALITE_GUIDE.md
   │  └── task.md
  ├── install.sh
  ├── install.sh.1
  ├── notebooks
   │  └── poi_without_cafes_heatmap.ipynb
  ├── README.md
  └── site_x_ui
     ├── components.json
     ├── data
      │  ├── all.geojson
      │  ├── banks.geojson
      │  ├── banks_final.csv
      │  ├── cafes.geojson
      │  ├── cafe_final.csv
      │  ├── d
      │  │  ├── banks.csv
      │  │  ├── compact_summary_images.csv
      │  │  ├── education.csv
      │  │  ├── health.csv
      │  │  ├── other.csv
      │  │  └── temples.csv
      │  ├── education.geojson
      │  ├── education_final.csv
      │  ├── health.geojson
      │  ├── health_final.csv
      │  ├── master_cafes_minimal.csv
      │  ├── other.geojson
      │  ├── other_final.csv
      │  ├── temples.geojson
      │  ├── temples_final.csv
      │  └── to-let
      │    ├── 1.jpg
      │    ├── 10.jpg
      │    ├── 2-2.jpg
      │    ├── 2.jpg
      │    ├── 3.jpg
      │    ├── 4.jpg
      │    ├── 5.jpg
      │    ├── 6.jpg
      │    ├── 7.jpg
      │    ├── 8.jpg
      │    ├── 9.jpg
      │    └── listings.csv
     ├── dist
      │  ├── assets
      │  │  ├── index-DqVkqJnd.js
      │  │  └── index-pVhnKmv1.css
      │  ├── index.html
      │  └── vite.svg
     ├── eslint.config.js
     ├── index.html
     ├── package-lock.json
     ├── package.json
     ├── public
      │  └── vite.svg
     ├── README.md
     ├── scripts
      │  ├── csv2geo.py
      │  ├── generate_dataset_index.py
      │  └── merge_cafes.js
     ├── src
      │  ├── App.css
      │  ├── App.tsx
      │  ├── assets
      │  │  └── react.svg
      │  ├── components
      │  │  ├── locationForm
      │  │  │  └── locationForm.tsx
      │  │  └── ui
      │  │    ├── button.tsx
      │  │    ├── card.tsx
      │  │    ├── chart-radar-lines-only.tsx
      │  │    ├── chart.tsx
      │  │    ├── input.tsx
      │  │    ├── label.tsx
      │  │    └── switch.tsx
      │  ├── index.css
      │  ├── lib
      │  │  └── utils.ts
      │  ├── main.tsx
      │  └── pages
      │    └── Result.tsx
     ├── tsconfig.app.json
     ├── tsconfig.json
     ├── tsconfig.node.json
     ├── tsconfig.tsbuildinfo
     └── vite.config.ts
```

### File List
- d:\projects\SiteX\install.sh
- d:\projects\SiteX\install.sh.1
- d:\projects\SiteX\README.md
- d:\projects\SiteX\backend\pois.json
- d:\projects\SiteX\backend\README.md
- d:\projects\SiteX\backend\requirements.txt
- d:\projects\SiteX\backend\RoadNetwork_Export.geojson
- d:\projects\SiteX\backend\road_network_interactive.html
- d:\projects\SiteX\backend\road_network_visualization.png
- d:\projects\SiteX\backend\sitex_geospatial.db
- d:\projects\SiteX\backend\__init__.py
- d:\projects\SiteX\backend\app\main.py
- d:\projects\SiteX\backend\app\__init__.py
- d:\projects\SiteX\backend\app\api\__init__.py
- d:\projects\SiteX\backend\app\api\endpoints\analysis.py
- d:\projects\SiteX\backend\app\api\endpoints\cafe_processing.py
- d:\projects\SiteX\backend\app\api\endpoints\explain.py
- d:\projects\SiteX\backend\app\api\endpoints\pois.py
- d:\projects\SiteX\backend\app\api\endpoints\predict.py
- d:\projects\SiteX\backend\app\api\endpoints\road_types.py

... and 4610 more files
