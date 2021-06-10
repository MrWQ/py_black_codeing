def getUniqueParams(self):
    # Initialize list
    parameter_array = []
    parameter_string_array = []
    messages = self.ctxMenuInvocation.getSelectedMessages()
    # This for loop iterates through all of the selected messages pulling out 
    # everything Burp considers a parameter (even cookies), and putting all of 
    # the parameters in an array
    for m in messages:
        request_byte_array = m.getRequest()
        requestInfo = self._helpers.analyzeRequest(request_byte_array)
        parameters = requestInfo.getParameters()
        parameter_array = parameter_array + parameters

    # This for loop iterates through each paramter and creates a string with the
    # paramname=paramvalue, so that they can be compared and sorted later.
    for p in parameter_array:
        param_string = p.getName() + "=" + p.getValue()
        # print "Param String:", param_string
        parameter_string_array.append(param_string)

    # After the for loop is finished, then uniquify and sort the parameters -- The main purpose of the extension
    unique_parameters = sorted(uniqify(self, parameter_string_array))

    print "************************************************************"
    print "******************** Unique Paramters **********************"
    print "************************************************************"
    print "************************************************************"
    print "******************** Unique Paramters **********************"
    print "************************************************************"
    print
    print "Number of Parameters:", len(parameter_string_array)
    print "Number of Unique Parameters :", len(unique_parameters)
    print

    param_dict = {}
    for unique_param in unique_parameters:
        # print "Param: %s" % (unique_param))
        param_name = unique_param.split("=")[0]
        param_value = unique_param.split("=")[1]
    # This if statement creates a dictionary, but unlike a normal dictionary, the value of each key is a list.
    # This is so that I can use the append function.
    # The key is the parameter name
    # The value is a list of all of unique the seen parameter values
        if not param_name in param_dict:
            param_dict[param_name] = []
            param_dict[param_name].append(param_value)

    for key, value in param_dict.iteritems():
        print(len(key) * "-" + "----")
        print("| %s |" % (key))
        print(len(key) * "-" + "----")
        for item in value:
            print(item)
        print("\n\n\n\n")


def uniqify(self, parameter_string_array):
    # not order preserving
    set = {}
    map(set.__setitem__, parameter_string_array, [])
    return set.keys()   