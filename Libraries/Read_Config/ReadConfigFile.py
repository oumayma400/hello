from jproperties import Properties
def aa():
    return True 
class ReadConfigFile():
    def read(PROJECT, key):
        configs  = Properties()
        configfile= '../Configurations/'+ str(PROJECT)+'_configuration.properties'
        with open(configfile, "rb") as read_prop:
            configs.load(read_prop)

        prop_view  = configs .items()
        print(type(prop_view))
        # for item in prop_view:
        #     print(item)
        #     print(item[0], '=', item[1].data)
        #print("url: ", configs.getmeta("url"))
        #print(configs.get("DB_User"))
        print(PROJECT)
        print(key + f': {configs.get(key).data}')

        return configs.get(key).data
