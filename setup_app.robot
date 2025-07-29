*** Settings ***
Library           AppiumLibrary
Test Teardown     Close Application

*** Keywords ***
Wait And Click Element
    [Arguments]    ${locator}
    ${element} =    Set Variable    ${locator}
    Wait Until Element Is Visible    ${element}    5s
    Click Element    ${element}
    Sleep    1s

*** Test Cases ***
Test Case Name
    Open Application    http://127.0.0.1:4723    platformName=Android    appium:deviceName=emulator-5554    appium:automationName=UIAutomator2    appium:udid=emulator-5554    appium:appActivity=com.google.android.apps.nexuslauncher.NexusLauncherActivity    appium:noReset=${True}    appium:appPackage=com.google.android.apps.nexuslauncher    appium:enableMultiWindows=${True}    appium:disableSuppressAccessibilityService=${True}    appium:ensureWebviewsHavePages=${True}    appium:nativeWebScreenshot=${True}    appium:newCommandTimeout=${3600}    appium:connectHardwareKeyboard=${True}
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnFreeTrial
    Wait And Click Element    id=com.android.permissioncontroller:id/permission_allow_button
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnAction
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnAction
    Wait And Click Element    id=com.android.permissioncontroller:id/permission_allow_button
    Wait And Click Element    id=com.android.permissioncontroller:id/permission_allow_button
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnAction
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnAction
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnAction
    Wait And Click Element    accessibility_id=grant_permission_dialog_allow_btn
    Wait And Click Element    id=com.android.settings:id/content_parent
    Wait And Click Element    android=new UiSelector().className("android.widget.RelativeLayout").instance(1)
    Wait And Click Element    id=android:id/switch_widget
    Wait And Click Element    id=android:id/accessibility_permission_enable_allow_button
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnAction
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnAction
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnAction
    Sleep    3s
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/btnAction
    Wait And Click Element    accessibility_id=main_feature_tabs_1_btn
    Wait And Click Element    id=com.trendmicro.fraudbuster:id/ivClose
    Wait And Click Element    accessibility_id=main_feature_tabs_home_btn

