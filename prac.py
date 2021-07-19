elif pressed == 'a': 
        print (json_data)
         #add
        def write_json(data, filename): 
            with open(filename,'w') as f: 
                json.dump(data, f, indent=4) 
            
  