<template>
  <b-card>
    <b-form @submit.stop.prevent="onSubmit">
      <b-form-group
        id="input-group-email"
        :label="$t('common.email.label_required')"
        label-for="input-email"
      >
        <b-form-input
          id="input-email"
          v-model="form.email"
          type="text"
          :placeholder="$t('common.email.placeholder')"
          autofocus
          trim
          required
        />
      </b-form-group>
      <b-form-group
        id="input-group-password"
        :label="$t('pages.register.password.label_required')"
        label-for="input-password"
      >
        <b-form-input
          id="input-password"
          v-model="form.password"
          type="password"
          :placeholder="$t('pages.register.password.placeholder')"
          trim
          required
        />
      </b-form-group>
      <b-form-group
        id="input-group-password"
        :label="$t('pages.register.password_repeat.label_required')"
        label-for="input-password"
      >
        <b-form-input
          id="input-password"
          v-model="form.password"
          type="password"
          :placeholder="$t('pages.register.password_repeat.placeholder')"
          trim
          required
        />
      </b-form-group>
      <b-button type="submit" variant="primary" class="card-link">
        {{ $t('common.nav.register') }}
      </b-button>
    </b-form>
  </b-card>
</template>

<script>
import { GlobalOverlay } from '@/mixins/global-overlay'
import { Form } from '@/mixins/form'
import { UpdateLocaleMutation } from '@/graphql/auth/update_locale.mutation'
import { RegisterMutation } from '@/graphql/auth/register.mutation' // Assuming you have a registration mutation
import { Auth } from '@/mixins/auth'

export default {
  mixins: [Auth, Form, GlobalOverlay],
  layout: 'card',
  middleware: ['redirect-if-authenticated'],
  data() {
    return {
      form: {
        email: this.$route.query.email || '',
        password: '',
      },
      redirect: this.$route.query.redirect || '',
    }
  },
  methods: {
    async onSubmit() {
      this.resetFormErrors()
      this.displayGlobalOverlay()

      try {
        const result = await this.$graphql.request(RegisterMutation, {
          email: this.form.email,
          password: this.form.password,
        })

        // You can perform additional actions if needed after successful registration.
        // Update user's locale if different from the
        // web application locale.
        if (result.login.locale !== this.$i18n.locale) {
          await this.$graphql.request(UpdateLocaleMutation, {
            locale: this.$i18n.locale.toUpperCase(),
          })

          result.login.locale = this.$i18n.locale
        }

        if (this.redirect !== '') {
          this.$router.push(this.redirect)
        } else {
          this.$router.push(this.localePath({ name: 'dashboard' }))
        }
      } catch (e) {
        this.hydrateFormErrors(e, true)
      } finally {
        this.hideGlobalOverlay()
      }
    },
  },
}
</script>
