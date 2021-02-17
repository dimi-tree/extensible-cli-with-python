Feature: showing off behave

  Scenario: run hello command
     Given we run the hello command with name argument
     Then the command returns "hello dimitri"
