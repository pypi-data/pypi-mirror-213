Project gregory~online~
=======================

*experimental code to online survey root spectra from THTTPServer*

**Last notice**: *changing to keybssh NOW*

Usage
-----

Based on \~/.config/gregory~online~/cfg.json

``` {.javascript org-language="js"}
{
 "placeholder": true,
 "filename": "~/.config/gregory_online/cfg.json",
 "spectrum": "b0c00",
 "udp_ip": "127.0.0.1",
 "server": "x.x.x.x",
 "poll_time": 5
}
```

it connects to

``` {.shell}
./bin_gregory_online.py
# OR override the server and spectrum name
./bin_gregory_online.py -s 127.0.0.1 -h b0c00
```

Install
-------

Github? *pip3 in future*

UI Components
-------------

There are two:

-   topbar
-   keyenter

The topbar runs in the background, provides two bars. The second one is
the keyboard input bar.

Engines of fetch
----------------

-   keep getting histo from server
-   keep historical spectra and be prepared to show dif
-   keep track of age and show rate
-   show bg spectrum rate for comparison

Version 2
=========

  ----------------------- ------------------------------
  histo~globalcont~.py    Container for histograms
  histo~npops~.py         operations between np ad th1
  histo~io~.py            load and save
  bin~gregoryonline~.py   
  config.py               
  fetchnp.py              
  getspe.py               
  key~enter~.py           
  mock~server~.py         
  rebin.py                
  setup.py                
  topbar.py               
  utilone.py              
  version.py              
  ----------------------- ------------------------------
