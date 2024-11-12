describe('template spec', () => {

  beforeEach(() => {
      cy.visit('/login/')
      cy.get('#username').type('testes')
      cy.get('#password').type('yuri1234')
      cy.get('.bg-purple-600').click()
  })

  it('escrever review e editar o texto', () => {
    cy.visit('/')
    cy.get(':nth-child(1) > .grid > :nth-child(1) > a > .w-368').click()
    cy.get('.mb-6 > .w-full').type('Teste')
    cy.get('.flex > .bg-gray-700').select('5')
    cy.get('.mb-6 > .flex > .text-center').click()
    
    cy.get('.m-2').should('have.text', 'Teste')
    cy.get('.text-blue-500 > .bi').click()
    cy.get('#modalComentario').type('Teste Editado')
    cy.get('.bg-blue-600').click()
    cy.get('.m-2').should('have.text', 'TesteTeste Editado')
    })

  it('escrever review sem nota e editar a nota', () => {
    cy.visit('/')
    cy.get(':nth-child(1) > .grid > :nth-child(1) > a > .w-368').click()
    cy.get('.mb-6 > .w-full').type('Teste')
    cy.get('.mb-6 > .flex > .text-center').click()
    cy.get('.justify-between > .space-x-4 > .font-semibold').should('have.text', 'testes') 
    cy.get('.text-yellow-500').should('have.text', '1 ⭐')
    cy.get('.m-2').should('have.text', 'Teste')
    cy.get('.text-blue-500 > .bi').click()
    cy.get('#modalRating').select('5')
    cy.get('.bg-blue-600').click()
    cy.get('.text-yellow-500').should('have.text', '5 ⭐')
    })

  it('escrever review e editar o texto e a nota', () => {
    cy.visit('/')
    cy.get(':nth-child(1) > .grid > :nth-child(1) > a > .w-368').click()
    cy.get('.mb-6 > .w-full').type('Teste')
    cy.get('.flex > .bg-gray-700').select('5')
    cy.get('.mb-6 > .flex > .text-center').click()
    cy.get('.justify-between > .space-x-4 > .font-semibold').should('have.text', 'testes')
    cy.get('.m-2').should('have.text', 'Teste')
    cy.get('.text-blue-500 > .bi').click()
    cy.get('#modalComentario').type('Teste Editado')
    cy.get('#modalRating').select('1')
    cy.get('.bg-blue-600').click()
    cy.get('.m-2').should('have.text', 'TesteTeste Editado')
    cy.get('.text-yellow-500').should('have.text', '1 ⭐')
  })

  afterEach(() => {
    cy.visit('/')
    cy.get(':nth-child(1) > .grid > :nth-child(1) > a > .w-368').click()
    cy.get('.text-red-500 > .bi').click()
  })

})
