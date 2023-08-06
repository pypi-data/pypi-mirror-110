# stark_middlewares

#### _Install package_
  ```
  pip install stark_middlewares
  ```

## _Usage_
##### 1. TrimMiddleware
- Add the below lines in settings.
  ```
  MIDDLEWARE += [
    stark_middlewares.middlewares.TrimMiddleware
  ]
  ```
  
##### 2. Maintenance Middleware
- Add the below lines settings.
  ```
  MIDDLEWARE += [
    stark_middlewares.middlewares.MaintenanceModeMiddleware
  ]
  ```
    i. If you want to add the site under maintenance mode set `IS_MAINTENANCE_MODE=True` in settings

    ii. You can whitelist the IP using `MAINTENANCE_IPS=[]` in settings

    iii. You can able to check the invalid IP using `SHOW_MAINTANCE_INVALID_IP=True` in settings.

    iv. You can able to skip some endpoint as well `SKIP_ENDPOINT=['login']` in settings.

##### 3. Rolewise Permission
- Add the below lines to add REST API Permission middleware
  ```
  MIDDLEWARE += [
    stark_middlewares.middlewares.UserRolePermission
  ]
    ```
  > DEFAULT ALLOWED_METHOD_PERMISSIONS:
    ALLOWED_METHOD_PERMISSIONS = {
        "list": "view_",
        "retrieve": "view_",
        "create": "add_",
        "partial_update": "change_",
        "delete": "delete_",
        "change_status": "change_",
        "bulk_delete": "add_",
    }

    If you want to add more permission you can just add ALLOWED_METHOD_PERMISSIONS in settings.
        e.g. `ALLOWED_METHOD_PERMISSIONS = {
            'get_list': 'add_'
        }`

    >> If you want to check the permission error then add SHOW_PERMISSION_ERROR=True in settings.

## License

MIT

**Stark Digital Media Services**