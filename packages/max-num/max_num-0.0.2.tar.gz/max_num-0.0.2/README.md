Project description

example:

   from max_num.max import Max

   ## check maximum number of undefined arguments 
   check_max_value = Max.max_num(1,23,11,2,4)
   print(check_max_value)

   ## check maximum number of a dictionary 
   sample_dict = {
      "Esharat" : 200,
      "Masum": 300,
      "Liza": 100,
      "Mahreen": 50,
   }
   check_max_dict_value = Max.max_num_dict(sample_dict)
   for (Key,Value) in check_max_dict_value.items():
         print(f"{key} got highest score: {Value}")
   
   ## Check maximum number of a list
   sample_list = [12,23,34,12,4,7,9,19]
   check_max_list_value = Max.max_num_list(sample_list)
   print(f"The bigest number is {check_max_list_value}")
