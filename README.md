# Python_sem4



  # Project name: Car price calculator. 
    
   ## Short description:
        Our project is made with the purpose of helping people get a fair valuation of their used car via using data from known car sales websites.
        The idea is to let the user enter his details about his car and he'll receive a rough estimate
        of what we believe to be the correct price based on our data and
        present him with both the estimate but also the plot showing our data so the know on how much data we based our answer on 
        giving them clear insight into the process.
    
    
   ## List of used technologies:
        OOP
        Plotting
        Exceptions
        Web scraping
        Data persistence
        Machine Learning (Linear regression)

   ## Libraries used:
        Matplotlib,
        Pandas,
        Numpy,
        Re — Regular expression operations,
        Selenium,
        Datetime,
        Sklearn,
        Io, 
        Argparse,
        Flask
    
   ## Installation guide (if any libraries need to be installed):
        Build docker enviroment as described her: https://github.com/Hartmannsolution/docker_notebooks
        If any of listed libraries ar missing, install them with pip install
    
    
   ## User guide (how to run the program):
        The program needs a database to be set while starting. To do so run the program from inside the root directory with python server.py - r = True
        To run the program in debug mode use command python server.py - p = False from root directory
        Both command can be combined. 
        For more info run python server.py -h
        
        Available endpoints:
        '/', GET : start page
        
        '/estimate' 'POST' gets json car: {model:string, year: int, km: int, capacity: float,fuel: string},
                returns : { recieved: car, estimated_price: int, intercept: float, coefficient: float}
         
        '/add', POST gets json : {model:string, year: int, km: int, capacity: float,fuel: string, price: int, user_name: string}
                returns json  added: {
                          capacity: float,
                          car_id: int, 
                          estimated_price: int,
                          fuel: String, 
                          km: int,  
                          model: string, 
                          owner: string, 
                          sale_price: int, 
                          year: int }
                          
         '/register' , POST gets json {user_name: string, password: string} 
                password must be at least 8 signs, has both upper and lover case , a digit and a special sign
                returns: {added: boolean, user_name: string}
                
                
                
          '/plot', GET, requires URL parameters : model, fuel, f1, f2, where f1 and f2 are the features to be used 
                                                  for visualization the price dependency of the two features
                                                  example: #/plot?model=A1&fuel=Benzin&f1=km&f2=capacity
                         returns 3d scatter plot (in the browser)

                
          
           
    
   ## Status (What has been done (and if anything: what was not done)):
        Completed:
       -  collectiong data with webscrapping
       -  data preparation
       -  linear regression
       -  data persistance (cars and users)
       -  data visualisation
       
       Missing:
       -  posting annoncements on web portals with Selenium
       -  error handling / user input validation
       -  there is hundrets of functionalities that could be implemented if there was time enough
       
    
   ## List of Challenges you have set up for your self (The things in your project you want to highlight):

      In terms of challenges, we had some issues with scrapping websites. 
      We were running into inconsistent errors while scraping which made it had to account for.
      
      Besides that, there were challenges in regards to rendering the plots to the user when using the endpoint. 
      The interaction between matplotlib and the server. 
      Should the plot should be rendered via the browser/server or should the server render the plot and save as image and return it.
      A lot of trial and error later, and we ended up with a function which returns the model which is then visible to the user in his/her brower.
