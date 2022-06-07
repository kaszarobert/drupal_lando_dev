# Run Drupal PHPUnit tests in Lando

This tutorial was made based on this article: https://agile.coop/blog/drupal-phpunit-tests-lando/

Edit: https://www.drupal.org/project/drupalci_environments/issues/3208793#comment-14431946 Since 2022-03-03 drupalci/webdriver-chromedriver was updated. That means new parameter must be added to the chromedriver command.


#### Setup

1. In .lando.yml under `services:` add:

  ```
  appserver:
    overrides:
      environment:
        SIMPLETEST_BASE_URL: "http://drupal1.lndo.site"
        SIMPLETEST_DB: "mysql://drupal9:drupal9@database/drupal9"
        BROWSERTEST_OUTPUT_DIRECTORY: '/app/web/sites/simpletest/browser_output'
        MINK_DRIVER_ARGS_WEBDRIVER: '["chrome", {"browserName":"chrome","chromeOptions":{"args":["--disable-gpu","--headless", "--no-sandbox", "--disable-dev-shm-usage"]}}, "http://chrome:9515"]'
  chrome:
    type: compose
    services:
      image: drupalci/webdriver-chromedriver:production
      command: chromedriver --log-path=/tmp/chromedriver.log --verbose --allowed-origins=* --whitelisted-ips=
  ```

  In environment variables we specify the URL, SQL database and user. Also check if the BROWSERTEST_OUTPUT_DIRECTORY exists. For some reason with this setup chromedriver cannot access the .localhost domain. That's why I'm using Lando's default .lndo.site. So, if you use localhost domains for appserver, don't forget to specify the Lando's one.

  ```
proxy:
  appserver:
    - drupal1.localhost
    - drupal1.lndo.site
  ```
  
2. Under `tooling:` add:

  ```
  testdebug:
    service: appserver
    cmd: "php /app/vendor/bin/phpunit -v -c /app/phpunit.xml"
  test:
    service: appserver
    cmd: "php /app/vendor/bin/phpunit -c /app/phpunit.xml"
  phpunit:
    service: appserver
    cmd: "/app/vendor/bin/phpunit"
  ```

3. Now, start the project with lando start and install Drupal with composer (the composer.json and vendor should be in the same folder as the .lando.yml file). You must also install the testing dependencies using composer:

  ```
lando composer require drupal/core-dev --dev --with-all-dependencies
lando composer require --dev phpspec/prophecy-phpunit
lando composer require --dev wikimedia/composer-merge-plugin
  ```

4. Edit composer.json and put this under the "extra" key: (this way we ensure that if a module requires other modules to be installed for testing, they should be downloaded, too)

  ```
        "merge-plugin": {
            "include": [
                "web/modules/contrib/*/composer.json",
                "web/themes/contrib/*/composer.json"
            ]
        }
  ```

5. Run `lando composer update` (Running with just `--lock` doesn't do anything for me)

6. Copy `web/core/phpcs.xml.dist` file to the root folder (it's where the .lando.yml is)!

  ```
  cp web/core/phpunit.xml.dist phpunit.xml
  ```

7. In this file you need to fix the bootstrap.php path to this:

  ```
<phpunit bootstrap="/app/web/core/tests/bootstrap.php" colors="true"
  ```
  Or by running this command:

  ```
sed -i 's|tests\/bootstrap\.php|/app/web/core/tests/bootstrap.php|g' phpunit.xml
  ```

8. Create the `web/sites/simpletest/browser_output` directory. When running browser tests, the output HTML will be saved here.

  ```
mkdir -p web/sites/simpletest/browser_output
  ```

9. You must rebuild the lando project: `lando rebuild -y`

10. If you want to run all the tests of a module (probably), not just one by one, you must fix the testsuite file paths in phpunit.xml. You must specify where are the tests relatively from the XML file. This XML structure can be different for each Drupal versions but here's a guide how the paths should be set:

```
  <testsuites>
    <testsuite name="unit">
      <file>web/core/tests/TestSuites/UnitTestSuite.php</file>
    </testsuite>
    <testsuite name="kernel">
      <file>web/core/tests/TestSuites/KernelTestSuite.php</file>
    </testsuite>
    <testsuite name="functional">
      <file>web/core/tests/TestSuites/FunctionalTestSuite.php</file>
    </testsuite>
    <testsuite name="functional-javascript">
      <file>web/core/tests/TestSuites/FunctionalJavascriptTestSuite.php</file>
    </testsuite>
    <testsuite name="build">
      <file>web/core/tests/TestSuites/BuildTestSuite.php</file>
    </testsuite>
  </testsuites>
  <listeners>
    <listener class="\Drupal\Tests\Listeners\DrupalListener">
    </listener>
  </listeners>
  <!-- Filter for coverage reports. -->
  <filter>
    <whitelist>
      <directory>web/includes</directory>
      <directory>web/lib</directory>
      <!-- Extensions can have their own test directories, so exclude those. -->
      <directory>web/modules</directory>
      <exclude>
        <directory>web/modules/*/src/Tests</directory>
        <directory>web/modules/*/tests</directory>
      </exclude>
      <directory>web/modules</directory>
      <exclude>
        <directory>web/modules/*/src/Tests</directory>
        <directory>web/modules/*/tests</directory>
        <directory>web/modules/*/*/src/Tests</directory>
        <directory>web/modules/*/*/tests</directory>
      </exclude>
      <directory>web/sites</directory>
     </whitelist>
  </filter>
```

#### Usage

Try the 4 types of tests - if everything will be green and OK, then it works. If you use  `lando testdebug` instead of `lando test` you will get much detailed error messages if some test fails or it's skipped.

```
lando test web/core/modules/node/tests/src/Unit/NodeOperationAccessTest.php
lando test web/core/modules/help/tests/src/Kernel/HelpEmptyPageTest.php
lando test web/core/modules/color/tests/src/Functional/ColorConfigSchemaTest.php
lando test web/core/modules/action/tests/src/FunctionalJavascript/ActionFormAjaxTest.php
```

You can also get a list of the available module tests:

```
lando test --list-groups
```

Here's how you specify which module's tests should be run:

```
lando test --group commerce,commerce_log,commerce_order,commerce_promotion,commerce_shipping,commerce_store
```

Or you can run tests by specifying the path to the module:

```
lando test web/modules/contrib/commerce
```