import { gql } from 'graphql-request'

export const RegisterMutation = gql`
  mutation register($email: String!, $password: String!) {
    register(email: $email, password: $password) {
      success
      message
    }
  }
`
