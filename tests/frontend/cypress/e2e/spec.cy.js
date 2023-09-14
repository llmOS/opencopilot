let generatedText;
describe('Frontend spec', {defaultCommandTimeout: 5000}, () => {
    it('Frontend loads', () => {
        cy.visit('http://127.0.0.1:3000/ui')
        cy.get('textarea').first().type('Hi{enter}')
        cy.wait(5000)
        cy.get('[class*="oc-mb-2"]').last().then(($value) => {
            generatedText = $value.text()
            cy.log("GOT text: " + generatedText)
            expect(generatedText).to.equal("User: Greetings!")
        })
    })
})
