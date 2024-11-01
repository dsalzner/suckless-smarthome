<html>
<head>
  <meta http-equiv="cache-control" content="no-cache" />
  <style>
  body {
      margin: 0mm 0mm 0mm 0mm;
      background-color: #1c1c1c;
  }
  .outer {
      border-radius: 8px;
      border: 0px solid black;
      background: #a4a4a4;
      
      padding-top: 8px;
      padding-bottom: 2px;
      padding-right: 6px;
      padding-left: 5px;
      
      max-width: 510px;
      max-height: 400px;
      
      margin: 2px;
      
      display: inline-block;
    }
    .inner {
      border-radius: 8px;
      background: #d2d2d2;

      padding-top: 2px;
      padding-bottom: 3px;
      padding-right: 5px;
      padding-left: 5px;

      margin-bottom: 8px;
      display: block;
    }
  </style>
</head>

<body>
<?php
//shell_exec("/home/codered/smarthome/automation_create_graphs.py");
?>

<div class="outer"><div class="inner""><img src="plot_fridge_cooler_24h.png" /></div></div>

<div class="outer"><div class="inner""><img src="plot_soil_einblatt-soil_a2-soil_a3-soil_b1-soil_b2-soil_b3-soil_b4-soil_b5_24h.png" /></div></div>

<div class="outer"><div class="inner""><img src="plot_temp_livingroom-temp_desk-temp_bedroom_24h.png" /></div></div>

<div class="outer"><div class="inner""><img src="plot_photovoltaics_batterycharge_24h.png" /></div></div>
<div class="outer"><div class="inner""><img src="plot_photovoltaics_solarpower_24h.png" /></div></div>
<div class="outer"><div class="inner""><img src="plot_photovoltaics_inverterpower_24h.png" /></div></div>
<div class="outer"><div class="inner""><img src="plot_fridge_power_24h.png" /></div></div>
<div class="outer"><div class="inner""><img src="plot_dishwasher-washingmaschine_power_24h.png" /></div></div>

<form method="post">
  <input type="submit" value="hue_tv_on" name="hue_tv_on">
  <input type="submit" value="hue_tv_off" name="hue_tv_off">
</form>

<?php
if(isset($_POST["hue_tv_on"])) {
  shell_exec("python3 /home/codered/smarthome/philips_hue.py --action seton --device Fernseher");
  echo("on");
}
if(isset($_POST["hue_tv_off"])) {
  shell_exec("python3 /home/codered/smarthome/philips_hue.py --action setoff --device Fernseher");
  echo("off");
}
?>
</body>
</html>
