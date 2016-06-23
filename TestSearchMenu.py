# -*- coding: utf-8 -*-
import unittest

from glsdp import GLBaseTestCase
from glsdp import GLSupportUI
from glsdp import GLWait
from glsdp import GLHelper
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

class TestSearchMenu(GLBaseTestCase, GLSupportUI):
    driverType = GLHelper.PHANTOMJS
    baseUrl = "http://www.rec-global.com"
    assertionErrors = []
    phrase = 'qa engineer'

    def glAfterSetUp(self):
        GLWait.whilePageLoaderIsVisible(self.driver)

    def glBeforeTearDown(self):
        #for s in self.assertionErrors:
            #print s
        pass

    def testHighlightedSearchPhrase(self):

        # Step 1
        self.driver.find_element_by_xpath("//*[@id='navigation-inner']/div[3]/div/form/div/a").click()
        # Verification Point 1
        searchMainTextfield = self.driver.find_element_by_xpath("//*[@id='mod-search-searchword']")
        self.assertTrue(searchMainTextfield.is_displayed())

        # Step 2
        self.focusOnElement(searchMainTextfield)

        # Step 3
        searchMainTextfield.send_keys(Keys.RETURN)
        GLWait.whilePageLoaderIsVisible(self.driver)
        # Verification Point 3
        assert u'' in self.driver.title
        searchButton = self.driver.find_element_by_xpath("//*[@id='searchForm']/fieldset[1]/section/div/div[2]/button")
        self.assertTrue(searchButton.is_displayed())

        # Step 4
        self.findElementAndPutText(self.driver,By.ID,'search-searchword',self.phrase)

        # Step 5
        self.driver.find_element_by_id('searchphraseexact').click()

        # Step 6
        searchButton.click()
        # Verification Point 6
        searchResultsNumber = self.driver.find_element_by_xpath("//*[@id='searchForm']/div/p/strong/span")
        for i in range(2, 2 * int(searchResultsNumber.text) + 2, 2):
            try:
                highlightedText = self.driver.find_element_by_xpath(
                    "//*[@id='blog-post-wrapper']/div[2]/div/div/div/dl/dd[" + str(i) + "]/span")
                # try:
                self.assertEqual(self.phrase.lower(), highlightedText.text.lower())
                # except AssertionError, e: self.verificationErrors.append(str(e))
            except NoSuchElementException:
                print 'Oferta bez podświetlonej frazy w tekście: nr ' + str(i / 2)


if __name__ == "__main__":
    unittest.main()
