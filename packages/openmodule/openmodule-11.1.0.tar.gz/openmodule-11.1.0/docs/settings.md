# SettingsProvider

SettingsProvider offers easy use of getting settings via the settings RPC. 
The SettingsProvider is thread-safe and implements caching of recently used settings 
together with invalidation triggered by message.

## Behavior

### Return values and Exceptions

Exceptions are thrown if a failure happens (timeout, conversion to target type failed, ...). 
If a settings is not found, None is returned. There exists functions with "_no_exception" postfix 
where exceptions are caught and logged and a fallback value is returned in this case.

### Caching

The values from cache are used if
 * a cached value is found for \<key\>/\<scope\>
 * the value is not expired (default is less than 300 seconds old)
 * the value can be parsed to the requested data type

Otherwise the value is requested with the RPC. All successfully retrieved values are put in the cache. 
In get_many all values are reloaded if one key is not found in cache.

## Usage

```python
settings = SettingsProvider()

# in get you can specify your return type for setting key/scope
result = settings.get(ResultType, "key1", "scope")
result = settings.get(List[Dict[str, int]], "key2", "scope")

# in get_many you can specify your return type for every setting you want to get in scope
relevant_settings = settings.get_many({"key1": ResultType, "key2": List[Dict[str, int]}, "scope")

# the no_exception functions catch exceptions and you can also specify a fallback value which is returned 
# in error cases or if not found (also overwrites None results). Default fallback is None
result = settings.get_no_exception(ResultType, "key1", "scope", fallback=ResultType())
results = settings.get_many_no_exception({"key1": ResultType, "key2": List[Dict[str, int]}, "scope", 
                                         fallbacks={"key1": ResultType()})
```
