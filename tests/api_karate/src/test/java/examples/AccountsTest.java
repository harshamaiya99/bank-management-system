package examples;

import com.intuit.karate.junit5.Karate;

// Class name must match the filename (AccountsTest)
class AccountsTest {

    @Karate.Test
    Karate testAccounts() {
        // This runs the "accounts.feature" file
        return Karate.run("accounts").relativeTo(getClass());
    }
}