# Remove exit errors from the config files that could trigger a warning
  
#sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ~/.config/chromium/'Local State'
  
#sed -i 's/"exited_cleanly":false/"exited_cleanly":true/; s/"exit_type":"[^"]\+"/"exit_type":"Normal"/' ~/.config/chromium/Default/Preferences

#chromium-browser  --noerrdialogs --disable-infobars --disable-session-crashed-bubble --incognito --homepage https://portal.kunindustries.com --kiosk http://czerwinski.pw/knpr/auto.html