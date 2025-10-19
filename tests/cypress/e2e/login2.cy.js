describe("Login Page Test", () => {

    it('Valid login', () =>{

        cy.visit("http://127.0.0.1:5000/login")
        cy.get("#username").type("hesha5@gmail.com")
        cy.get("#password").type("123456")
        cy.get("#submit").click()

        cy.contains("Welcome to the Weather App!").should("be.visible")

    })

    it('Invalid login', () => {
        cy.visit("http://127.0.0.1:5000/login")
         cy.get("#username").type("hesha0709@gmail.com")
        cy.get("#password").type("12345")
        cy.get("#submit").click()

        cy.get(".flashes").should("contain", "Invalid username or password.")

    })

})