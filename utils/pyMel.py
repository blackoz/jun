import inspect
import pymel.core as pm
import pymel.tools.mel2py as mel2py

def mel2pyDialog():
    """ this convert mel to python file.
   
    how to use:
    from rigWorkshop.ws_user.jun.utils import pyMel
    #mel to pymel convertor.
    pyMel.mel2pyDialog()
    """
    
    result = pm.promptDialog(
                    title='mel2py convertor',
                    message='Enter Name:',
                    button=['OK', 'Cancel'],
                    defaultButton='OK',
                    cancelButton='Cancel',
                    dismissString='Cancel')
    
    if result == 'OK':
            text = pm.promptDialog(query=True, text=True)
            
            # Get the PyMel equivalent
            pmAnswer = mel2py.mel2pyStr(text, pymelNamespace='pm')
            
            # Get rid of the old way
            pmCode = pmAnswer.replace("pymel.all", "pymel.core")
            print (pmCode)

def get_class_that_define_method(meth):
    """check out where the method comes from
    str method: specify method you want to query
    
    how to use:
        get_class_that_define_method(jnt[0].boundingBox)
        get_class_that_define_method(jnt[0].getMatrix)
        get_class_that_define_method(jnt.lower)
    """
    for cls in inspect.getmro(meth.im_class):
        if meth.__name__ in cls.__dict__:
            return cls
    return None
