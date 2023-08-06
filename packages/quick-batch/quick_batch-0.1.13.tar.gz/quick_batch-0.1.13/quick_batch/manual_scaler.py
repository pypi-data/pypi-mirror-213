from utilities.manage_services import update_processor_service


def scaler(num_processors=None):
    # check num_processors is an integer
    try:
        num_processors = int(num_processors)
    except ValueError:
        raise ValueError("FAILURE: num_processors must be an integer")

    # check basic value of num_processors
    if num_processors < 1:
        raise ValueError("FAILURE: num_processors must be greater than 0")

    # print update
    print("INFO: manual default scale override --> " +
          "scaling processor service " + str(num_processors) +
          " to  instances...")

    # scale up processor service
    update_processor_service(num_processors)

    # print update
    print("INFO: ...complete")
