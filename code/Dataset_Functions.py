
import pickle
def write_list(a_list, name):
    """
        store list in binary file so 'wb' mode

        Parameters
        ----------
        name : string
            the wanted file name of the list
        a_list : list
            the list that we want to save
    """
    with open(name, 'wb') as fp:
        pickle.dump(a_list, fp)
        print('Done writing list into a binary file')

def read_list(name):
    """
       for reading file and extract list

       Parameters
       ----------
       name : string
           path to the list file

       Returns
       -------
       n_list : list
           the list save in file
    """
    #
    with open(name, 'rb') as fp:
        n_list = pickle.load(fp)
        return n_list