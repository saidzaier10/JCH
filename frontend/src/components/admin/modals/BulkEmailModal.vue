<script setup>
import { ref } from 'vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseTextarea from '@/components/ui/BaseTextarea.vue'
import api from '@/utils/axios'
import { useToastStore } from '@/stores/toast'

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true
    },
    selectedMembers: {
        type: Array, // Array of IDs
        required: true
    },
    allMembers: {
        type: Array, // Array of Member objects for name resolution
        required: true
    },
    initialSubject: {
        type: String,
        default: ''
    },
    initialBody: {
        type: String,
        default: ''
    }
})

const emit = defineEmits(['close', 'sent'])

const toast = useToastStore()
const sendingEmail = ref(false)
const form = ref({
    subject: props.initialSubject,
    body: props.initialBody
})

const getRecipientPreview = () => {
    if (props.selectedMembers.length === 0) return ''
    const firstFew = props.selectedMembers.slice(0, 3).map(id => {
        const member = props.allMembers.find(m => m.id === id)
        return member ? `${member.first_name} ${member.last_name}` : 'Inconnu'
    })
    const remaining = props.selectedMembers.length - 3
    if (remaining > 0) {
        return `${firstFew.join(', ')} et ${remaining} autres...`
    }
    return firstFew.join(', ')
}

const send = async () => {
    sendingEmail.value = true
    try {
        await api.post('/api/emails/bulk-send/', {
            member_ids: props.selectedMembers,
            subject: form.value.subject,
            body: form.value.body
        })
        toast.success('Emails envoyés avec succès')
        emit('sent')
        emit('close')
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de l'envoi des emails")
    } finally {
        sendingEmail.value = false
    }
}
</script>

<template>
    <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog"
        aria-modal="true">
        <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                @click="$emit('close')"></div>
            <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div
                class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                        Envoyer un email groupé
                    </h3>
                    <p class="text-sm text-gray-500 mb-4">
                        Envoi à {{ selectedMembers.length }} destinataires.
                    </p>
                    <div class="mb-4 p-3 bg-gray-50 rounded-lg text-sm text-gray-600">
                        <span class="font-medium">Destinataires :</span>
                        {{ getRecipientPreview() }}
                    </div>
                    <form @submit.prevent="send" class="space-y-4">
                        <BaseInput id="email-subject" label="Sujet" v-model="form.subject" required
                            placeholder="Sujet de l'email" />
                        <div>
                            <BaseTextarea id="email-body" label="Message" v-model="form.body" rows="6" required
                                placeholder="Votre message..." />
                        </div>
                        <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                            <BaseButton type="submit" variant="primary" :loading="sendingEmail"
                                class="w-full sm:col-start-2">
                                Envoyer
                            </BaseButton>
                            <BaseButton type="button" variant="white" @click="$emit('close')"
                                class="mt-3 w-full sm:mt-0 sm:col-start-1">
                                Annuler
                            </BaseButton>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
