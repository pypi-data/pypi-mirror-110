=====
Usage
=====

To use PiView in a project::

    import piview

Import the required components::

    from piview.CPU import CPU
    from piview.GPU import GPU
    from piview.Hardware import Hardware
    from piview.Host import Host
    from piview.Network import Network
    from piview.Storage import Storage

Access the component methods as required::

    # obtain the status of the i2c channel
    hw_i2c = Hardware.i2c()
