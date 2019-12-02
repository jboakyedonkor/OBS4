/// <reference types="Cypress" />

context('OBS',() =>{
    const email = "test1@gmail.com"
    const password = "welp"

    const badEmail = "test2@gmail.com"
   
    beforeEach(() => {
        cy.visit('http://localhost:5000/')
      })
    it('It has a title', () => {
        cy.contains("OBS")
    })
    it('Happy Path Success',() =>{
        cy.get('#email').type(email)
        cy.get('#password').type(password)
        cy.get('#submit').click()
        cy.contains("Logout")
    })
    it('Failure Case',() =>{
        cy.get('#email').type(badEmail)
        cy.get('#password').type(password)
        cy.get('#submit').click()
        cy.contains("Logout")
    })
})