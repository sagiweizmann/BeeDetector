import { gql } from 'graphql-request'
import { MeFragment } from '@/graphql/auth/me.fragment'

export const RegisterMutation = gql`
  mutation register($email: String!, $firstName: String!, $lastName: String!, $password: String!) {
    register(email: $email,firstName: $firstName,lastName: $lastName, password: $password) {
    ...MeFragment
    }
  }
  ${MeFragment}
`
