from model import Model
from view import View
from controller import Controller
   
# Driver for MVC
controller = Controller()
view = View(controller)
model = Model(controller)
controller.linkView(view)
controller.linkModel(model)

# Passing the control to the controller
controller.start()
