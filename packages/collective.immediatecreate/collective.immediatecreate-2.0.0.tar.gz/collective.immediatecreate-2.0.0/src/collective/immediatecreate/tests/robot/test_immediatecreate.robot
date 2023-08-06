# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.immediatecreate -t test_example.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.immediatecreate.testing.COLLECTIVE_IMMEDIATECREATE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/collective/immediatecreate/tests/robot/test_example.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  plone.app.robotframework.keywords.Debugging
Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

#Scenario: As a member I want to be able to log into the website
 # [Documentation]  Example of a BDD-style (Behavior-driven development) test.
  #Given a login form
   #When I enter valid credentials
   #Then I am logged in

Scenario: A new folder is added
  Given logged in
    When create folder
    Then Location Should Contain  new-folder

Scenario: Cancel the new folder
  Given logged in
  and create folder
	and wait until element is visible  css=div.formControls
		When Click Button  css=div.formControls > input#form-buttons-cancel
		Then Click Link  css=li#contentview-folderContents > a
		and Page Should Not Contain  New Folder

Scenario: Bild in Ordner
  Given logged in
  and create folder
	and wait until element is visible  css=label.horizontal
		When Input Text  css=div#formfield-form-widgets-IDublinCore-title > input#form-widgets-IDublinCore-title  New Folder
		and wait until element is visible  css=div#mceu_15
		and Click Button  css=div#mceu_15 > button#mceu_15-button
		and wait until element is visible  css=div.plone-modal-body
		and Click Link  css=nav.autotoc-nav > a#tinymce-autotoc-autotoc-1
		wait until element is visible  css=div.col-md-9
		and Execute Javascript  dzoption = $(".upload-area")[0].dropzone.options;dzoption.forceFallback = true;$(".upload-area")[0].dropzone.destroy();$(".upload-area").dropzone(dzoption)
		and Choose File  css=div.dz-fallback input[type=file]  ${CURDIR}/test_image.jpg
    and Execute Javascript  $('.upload-area form').ajaxSubmit()
		Then Click Link  css=nav.autotoc-nav > a#tinymce-autotoc-autotoc-0
		and Click Link  xpath=//fieldset[@data-linktype='image']//div[@class='pattern-relateditems-container']//a[@href='/new-folder' and @class='crumb']
		and Click Link  xpath=//div[@class='pattern-relateditems-result']//a[@class='pattern-relateditems-result-select selectable']
		and Click Button  xpath=//div[@class='pattern-modal-buttons']//input[@class='plone-btn plone-btn-primary context']
		and Click Button  css=div.formControls > input#form-buttons-save
		and Page Should Contain Image  xpath=//img[@title='test_image.jpg']


*** Keywords *****************************************************************

logged in
  Given Go to homepage
  and Log in as site owner
  and wait until element is visible  css=li#plone-contentmenu-factories

create folder
	Click Link  css=li#plone-contentmenu-factories > a
  and Click Link  css=li.plonetoolbar-contenttype > a#folder

# --- Given ------------------------------------------------------------------

a login form
  Go To  ${PLONE_URL}/login_form
  Wait until page contains  Login Name
  Wait until page contains  Password


# --- WHEN -------------------------------------------------------------------

I enter valid credentials
  Input Text  __ac_name  admin
  Input Text  __ac_password  secret
  Click Button  Log in


# --- THEN -------------------------------------------------------------------

I am logged in
  Wait until page contains  You are now logged in
  Page should contain  You are now logged in
