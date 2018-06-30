import tweepy
import csv
import os
import getpass
from simplecrypt import encrypt, decrypt


class Authorizer:

    def __init__(self, user_arg=-1):
        '''
        Sets up instance variable username
        :param user_arg: optional argument for a username
        '''
        # set username to user_arg
        if(isinstance(user_arg, str)):
            self.username = user_arg.strip()
        else:
            self.username = user_arg

        # create absolute path to profile
        abs_path = os.path.abspath(os.path.dirname(__file__))
        path_list = abs_path.split('/')
        path_list[-1] = "profiles"
        self.path = '/'.join(path_list)

        # set up profiles directory
        if(not os.path.exists(self.path)):
            os.makedirs(self.path)

    def authorize(self):
        '''
        Walks the user through either creating a new user, or logging into a previous one
        User files are saved as username.enc and contain an encrypted string containing the
        user's tokens
        Also handles checking with verification method (tokens or link) the user will use
        :return: an OAuthHandler object that can be used to create an API object
        '''

        # get username
        if (self.username == -1):
            str_name = str(self.username)
            while( not str_name.isalnum()):
                print("Please enter a user name for Tweetsole: ", end='')
                str_name = input().strip()
            self.username = str_name
        else:
            print("Welcome {}".format(self.username))

        # check if user has password
        if((self.user_exists() and self.has_password()) or not self.user_exists() ):
            # if so, or if they don't have an account, get password
            password = self.get_password()
            # enter password as -1 if you don't want one
        else:
            # else, handle_user w/o password
            password = -1


        # get tokens, if they exist
        consumer_token, consumer_secret, access_token, access_secret = self.handle_user(password)

        #authorize app
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_token, access_secret)
                        
        
        #check tokens using api call
        try:
            api = tweepy.API(auth)
            api.home_timeline()
        except:
            #remove user history, try again
            if(self.has_password()):
                os.remove(self.path + "/{}.enc".format(self.username))
            else:
                os.remove(self.path + "/{}.csv".format(self.username))

            print("Invalid tokens, deleting user profile. Please try again.")
            self.authorize()

        return auth

    def get_password(self):
        '''
        Gets the user's password, or helps user create one
        :return: a password as a string
        '''

        # if it exists, don't confirm
        if (self.user_exists()):
            password = getpass.getpass("Password: ")
        else:
            # if its a new password, have user enter it twice
            if(self.ask_for_password()):
                password = 0
                password_reenter = 1
                while (password != password_reenter):
                    password = getpass.getpass("Please create a password: ")
                    password_reenter = getpass.getpass("Please re-enter password: ")
                    if (password != password_reenter): print("Passwords do not match, try again!")
            else:
                password = -1

        return password

    def ask_for_password(self):
        '''
        Asks new users if they would like to use a password
        :return: Returns true if the user wants to use a password,
                false if they do not want to use a password
        '''
        print("Would you like to use a password to secure your API credentials? (y/n) ", end='')
        yes_no = input()
        while(yes_no != 'y' and yes_no != 'n'):
            print("Please enter either y or n: ", end = '')
            yes_no = input()

        if(yes_no == "y"):
            return True
        else:
            return False

    def get_tokens(self, password):
        '''
        Gets the four tokens needed for authentication, encrypts them as a string in username.enc

        :param password: the user's password to encrypt the tokens
        :return: unencrypted consumer_token, consumer_secret, access_token, access_secret
        '''

        print("Would you like to verify by generating access tokens, or by a one-time link? Enter tokens or link: ",
              end='')
        method = input().strip()

        while (method != "link" and method != "tokens"):
            print("Invalid input, please try again. Enter tokens or link: ", end='')
            method = input().strip()

        if (method == "link"):
            verify = True
        else:
            verify = False

        print("Please authorize Tweetsole with Twitter at apps.twitter.com")
        print("Create a new application and jot down the consumer token and consumer secret")
        
        print("Please enter the consumer token: ", end = '')
        consumer_token = input().strip()
        print("Please enter the consumer secret: ", end = '')
        consumer_secret = input().strip()

        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)        

        if(not verify):
            access_token, access_secret = self.get_access_tokens()
        else:
            access_token, access_secret = self.get_verification_pin(auth)
    
        # data structure for password files
        token_list = [consumer_token, consumer_secret, access_token, access_secret]

        # if password != -1,  encrypt
        if(password != -1):
            return self.encrypt_tokens(password, token_list)
        else:
            return self.store_tokens(token_list)

    def split_keys(self, keys_list ):
        '''
        Takes a list of keys and splits them into variables
        :param keys_list: a list of API tokens
        :return: the four API tokens needed to authenticate the user
        '''
        consumer_token = keys_list[0]
        consumer_secret = keys_list[1]
        access_token = keys_list[2]
        access_secret = keys_list[3]

        return consumer_token, consumer_secret, access_token, access_secret

    def store_tokens(self, keys_list):
        '''
        Stores a list of tokens in a CSV file for users without passwords
        :param keys_list: a list of API tokens
        :return: the four API tokens needed to authenticate the user
        '''
        file = open(self.path + "/{}.csv".format(self.username), 'w')
        with file:
            writer = csv.writer(file)
            writer.writerow(keys_list)

        return self.split_keys(keys_list)

    def encrypt_tokens(self, password, keys_list):
        '''
        Encrypts a list of tokens in a .enc file for users with passwords
        :param password: the user's password
        :param keys_list: the four API tokens needed to authenticate the user in a list
        :return: the four API tokens needed to authenticate the user
        '''
        # add user info to user.csv
        # make list a comma separated string, encrypt it
        token_string = ','.join(keys_list)
        print("Encrypting tokens...")
        ciphertext = encrypt(password, token_string.encode())
        encrypted_file = open(self.path + "/{}.enc".format(self.username), 'wb')
        encrypted_file.write(ciphertext)

        return self.split_keys(keys_list)

    def get_verification_pin(self, auth):
        '''
        Gets the URL to get the verification pin
        :param auth: the OAuthHandler object that, when given a pin, produces access tokens
        :return: the access_token and access_secret for the user
        '''

        # get verification url                                                                                                                                                   
        try:
            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError:
            print("Error: failed to get request url")

        #get verification pin                                                                                                                                                    
        print("Please follow {} to get a verification pin".format(redirect_url))
        print("Enter verification pin: ", end = '')
        verifier = input().strip()

        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError:
            print('Error! Failed to get access token.')

        access_token = auth.access_token
        access_secret = auth.access_token_secret
        
        return access_token, access_secret

    def get_access_tokens(self):
        '''
        Gets the access tokens directly from the user
        :return: the access_token and access_secret
        '''
        print("Under your app in Twitter, go to Keys and Access Tokens > Token Access > Create my access token")
        print("Please enter the access token: ", end = '')
        access_token = input().strip()
        print("Please enter the access token secret: ", end = '')
        access_secret = input().strip()
    
        return access_token, access_secret

    def handle_user(self, password):
        '''
        Handles returning the tokens if the user exists
        Otherwise, calls get_tokens()
        :param password: the user's password
        :return: consumer_token, consumer_secret, access_token, access_secret
        '''

        # if user exists, decrypt username.enc and return decrypted tokens
        if(self.user_exists()):
            try:
                if(password != -1):
                #if password != -1, decrypt
                    return self.decrypt_user(password)
                # else get_csvtokens()
                else:
                    return self.get_csv_tokens()
            except:
                # if there is an issue with the file
                print("User file corrupted, removing {}".format(self.username))
                if(self.has_password()):
                    os.remove(self.path + "/{}.enc".format(self.username))
                else:
                    os.remove(self.path + "/{}.csv".format(self.username))

                exit(2)
        else:
            # signals that user does not exist
            return self.get_tokens(password)

    def get_csv_tokens(self):
        '''
        Gets the API credentials from an existing user's user.csv file
        :return: the four API tokens needed to authenticate the user
        '''
        # open csv file for reading
        file = open(self.path + "/{}.csv".format(self.username), 'r')
        with file:
            reader = csv.reader(file, delimiter=',', quotechar=',',quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                # for row, put list into tokens_list variable
                tokens_list = row

        # return split tokens
        return self.split_keys(tokens_list)

    def decrypt_user(self, password):
        '''
        Decrypts the username.enc file, formats it into a list of tokens
        :param username: the chosen username
        :param password: the user's password
        :return: a list of the API tokens needed to authenticate the user
        '''

        #if(password != -1):
        #decrypt string in username.enc
        encrypted_file = open(self.path + "/{}.enc".format(self.username), 'rb').read()
        print("Decrypting tokens...")
        keys_string = decrypt(password, encrypted_file).decode()

        # create list, splitting decrypted string at the commas
        api_keys = keys_string.split(',')

        return self.split_keys(api_keys)

    def user_exists(self):
        '''
        Checks if a user's .enc or .csv file exists
        :param username: the chosen username
        :return: True if it exists, false if otherwise
        '''

        # try to read file in dict structure
        if( os.path.isfile(self.path + "/{}.enc".format(self.username))
            or os.path.isfile(self.path + "/{}.csv".format(self.username)) ):
            return True
        else:
            return False

    def has_password(self):
        '''
        Checks if the user is using a password to encrypt their credentials
        :param username: the chosen username
        :return: True if the user has encrypted their credentials with a password,
                False if they are not using a password
        '''
        if(os.path.isfile(self.path + "/{}.enc".format(self.username))):
            return True
        elif(os.path.isfile(self.path + "/{}.csv".format(self.username))):
            return False
