import bcrypt


def hash_password(password):
    """
    Hashes a password using bcrypt library.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password as a string.
    """
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Return the hashed password as a string
    return hashed_password.decode('utf-8')


def verify_password(password, hashed_password):
    """
    Verifies if a password matches a hashed password using bcrypt library.

    Args:
        password (str): The password to be verified.
        hashed_password (str): The hashed password to be compared against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.
    """
    really_hashed_password = hashed_password[0][0]
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), really_hashed_password.encode('utf-8'))

# ####################
# ##    REGISTER    ##
# ####################


# # Requete à faire à la DB lors de l'enregistrement
# receive_password = input("Register, enter a password : \n")
# hash_to_send = hash_password(receive_password)
# print(hash_to_send)
# # Requete d'envoi de la DB de pwd_to_send pour l'enregistrer
# print("You have been successfully register")

# ####################
# ##     LOGIN      ##
# ####################
# login_input = input("Enter a password : \n")
# # Requete dans la DB pour récupérer le hash de l'utilisateur (ici hash_to_send)
# resolve = verify_password(login_input, hash_to_send)
# if(resolve):
#     # Login successful
#     print("You have been succesfully logged")
# else:
#     # Wrong pwd
#     print("wrong pwd")
