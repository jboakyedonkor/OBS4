/// <reference types="Cypress" />

context('OBS', () => {
    const username = "assign2"
    const email = "assign2@gmail.com"
    const password = "ggggggggg"

    const badEmail = "test1@gmail.com"
    const badPassword = "www"
    const fundAmount = 10000
    const aaplShareAmount = 20


    // #Integration
    it('It has a title', () => {
        cy.visit('http://localhost:5000/')
        cy.contains("OBS")
    })
    // #Integration
    it('Register for an account', () => {

        cy.get('#register').click()
        cy.get('#username').type(username)
        cy.get('#email').type(email)
        cy.get('#password').type(password)
        cy.get('#confirm_password').type(password)
        cy.get('#submit').click()
        cy.contains("Your account has been created! You are now able to log in")
    })
    // it('Failure Case to login/ Bad Password',() =>{
    //     cy.get('#email').type(badEmail)
    //     cy.get('#password').type(badPassword)
    //     cy.get('#submit').click()
    //     cy.contains("Login Unsuccessful. Please check email and password")
    // })

    // #Integration
    it('Login with just registered account Success', () => {
        cy.get('#login').click()
        cy.get('#email').type(email)
        cy.get('#password').type(password)
        cy.get('#submit').click()
        cy.get('#dashboard').click()

        // cy.contains("Logout")
    })
    // it('Add funds',() =>{
    //     cy.get('#login').click() 
    //     cy.get('#email').type(email)
    //     cy.get('#password').type(password)
    //     cy.get('#submit').click()
    //     cy.get('#dashboard').click() 

    //     cy.get('#addFundsButton').click() 
    //     cy.get('#fundAmount').type(fundAmount)
    //     cy.contains('Confirm').click()
    //     cy.contains('Cash:'+fundAmount)
    // })
    // it('Make a purchase',() =>{
    //     cy.get('#aaplShareAmount').type(aaplShareAmount)
    //     cy.get('#aaplBuyButton').click() 
    //     cy.wait(2000)
    //     cy.get('totAAPLShares').contains(aaplShareAmount)


    // })
    //     it('Sell Shares',() =>{
    //         cy.get('#aaplShareAmount').type(aaplShareAmount-10)
    //         cy.get('#aaplSellButton').click() 
    //         cy.wait(6000)
    //         cy.get('totAAPLShares').contains(aaplShareAmount-10)


    // #Integration
    it('Transaction Page', () => {
        cy.contains('Transactions').click()

        // cy.get('#login').click() 
        // cy.get('#email').type(email)
        // cy.get('#password').type(password)
        // cy.get('#submit').click()

    })
})