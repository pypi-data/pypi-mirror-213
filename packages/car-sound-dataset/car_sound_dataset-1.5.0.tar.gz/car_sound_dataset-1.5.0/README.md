# car_sound_dataset
This repo contains the source code of car sound dataset Python package.

https://pypi.org/project/car-sound-dataset/

# How to install?
pip install car-sound-dataset

# About the dataset
The dataset contains 17121 car sound events. Each event is recorded by at least 1 and maximum 6 devices.
The length of each recording is 3 sec. The sample frequency was 3906 Hz during the measurements.
You can download the dataset and select different recordings with this package. 

# Class


 
        A class used to represent the car sound dataset.

        ...

        Attributes
        ----------
        path : str
            A path, where you want to download and use the dataset.
            The default path is the current working directory.
            
            
           
# Methods

        download_and_get_dataset()
            Downloads the dataset and the json file, which identifies the events.

        list_events_of_dict( car_dataset_dict)
            This method prints to console the event IDs of a car_dataset_dict.
            
        plot_event(car_dataset_dict, event_id)
            You can plot an event with this method.

        play_event(car_dataset_dict, event_id, nomralize=True)
            You can play the recordings of an event with this method.

        filter_by_pattern(car_dataset_dict, pattern)
            This method helps you to select events by a pattern.
            The pattern should contain 'X', '0' or '1'.
            'X' - You don't care, if the device recorded the event or not.
            '0' - You skip the recordings of this device.
            '1' - This device recorded the event.
            You have to give the pattern as a list. Each list element represents each device.
            An example pattern: ['0', '1', 'X', '0', 'X', '1']
            This means we skip the recordings of DEVICE1 and DEVICE4. We select the events,
            where DEVICE2 and DEVICE6 recorded the event. Each event will contain 2-4 recordings.
            It depends on DEVICE3 and DEVICE5. If one of DEVICE3 and DEVICE5 recorded the event,
            the event will contain 3 recordings and if both is recorded the event, it will contain
            4 recordings.

        filter_by_exact_device_count(car_dataset_dict, device_count)
            This method selects the events, which is recorded by the given count of devices.

        filter_by_min_device_count(car_dataset_dict, device_count)
            This method selects the events, which is recorded by at least the given count of devices.

        load_dict_as_pool(car_dataset_dict)
            This method loads the recordings into a 3D numpy array. In this case each element
            contains only one recording. The recordings of an event are split to single recordings.

        load_dict(car_dataset_dict, is_random = False, device_indexes = [])
            This method loads the recordings into a 3D numpy array. In this case each element
            contains events. One event usually contains more than one recordings.


    

