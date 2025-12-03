<template>
    <div class="flex h-screen bg-gray-100 font-sans">
        <!-- Sidebar -->
        <div class="w-64 bg-judo-blue text-white flex flex-col shadow-2xl relative overflow-hidden">
            <div class="absolute inset-0 bg-linear-to-b from-blue-900/50 to-transparent pointer-events-none"></div>
            <div class="p-6 border-b border-blue-800/50">
                <div class="flex items-center space-x-2">
                    <div class="w-10 h-10 bg-white/10 rounded-lg flex items-center justify-center">
                        <span class="text-2xl">🥋</span>
                    </div>
                    <div>
                        <h1 class="text-xl font-bold tracking-wide">Judo Club Hem</h1>
                        <p class="text-xs text-blue-200">Administration</p>
                    </div>
                </div>
            </div>
            <nav class="flex-1 p-4 space-y-1">
                <a href="#" @click.prevent="currentTab = 'dashboard'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'dashboard' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <LayoutDashboard :size="20" class="mr-3" />
                    <span>Vue d'ensemble</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'members'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'members' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <Users :size="20" class="mr-3" />
                    <span>Membres</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'registrations'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'registrations' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <ClipboardList :size="20" class="mr-3" />
                    <span>Inscriptions</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'finances'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'finances' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <Wallet :size="20" class="mr-3" />
                    <span>Finances</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'events'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'events' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <Calendar :size="20" class="mr-3" />
                    <span>Événements</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'attendance'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'attendance' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <ClipboardCheck :size="20" class="mr-3" />
                    <span>Présences</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'seasons'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'seasons' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <Settings :size="20" class="mr-3" />
                    <span>Saisons & Catégories</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'gallery'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'gallery' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <ImageIcon :size="20" class="mr-3" />
                    <span>Galerie</span>
                </a>
                <a href="#" @click.prevent="currentTab = 'users'"
                    class="flex items-center px-4 py-3 rounded-lg transition-all duration-200 group"
                    :class="currentTab === 'users' ? 'bg-white/15 text-white font-medium shadow-lg' : 'text-blue-100 hover:bg-white/10 hover:text-white'">
                    <UserCog :size="20" class="mr-3" />
                    <span>Utilisateurs</span>
                </a>
            </nav>
            <div class="p-4 border-t border-blue-800/50">
                <button @click="logout"
                    class="w-full flex items-center justify-center px-4 py-2 text-sm text-blue-200 hover:text-white hover:bg-white/10 rounded-lg transition">
                    <LogOut :size="18" class="mr-2" />
                    Déconnexion
                </button>
            </div>
        </div>

        <!-- Content -->
        <div class="flex-1 overflow-auto">
            <div class="p-8 max-w-7xl mx-auto">
                <!-- Dashboard Tab -->
                <!-- Dashboard Tab -->
                <div v-if="currentTab === 'dashboard'">
                    <DashboardStats :stats="stats" :registrations="registrations" :loading="loading" />
                </div>

                <!-- Members Tab -->
                <div v-if="currentTab === 'members'">
                    <div class="flex justify-between items-center mb-6">
                        <div>
                            <h2 class="text-2xl font-bold text-gray-900">Gestion des Membres</h2>
                            <p class="text-gray-500">{{ allMembers.length }} membres au total</p>
                        </div>
                        <BaseButton variant="primary" @click="openCreateUserModal">
                            <template #icon>
                                <Plus :size="20" />
                            </template>
                            Nouveau Membre
                        </BaseButton>
                    </div>

                    <MembersTable :members="allMembers" :registrations="registrations" :categories="categories" :loading="loadingMembers"
                        @edit-member="openEditMemberModal" @weigh-in="openWeighInModal"
                        @send-email="handleBulkEmailAction" @export-excel="exportExcel" />
                </div>

                <!-- Finances Tab -->
                <div v-if="currentTab === 'finances'">
                    <div class="mb-6">
                        <h2 class="text-2xl font-bold text-gray-900">Gestion Financière</h2>
                        <p class="text-gray-500">Suivi des paiements et revenus</p>
                    </div>

                    <!-- Financial KPIs -->
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                        <BaseCard class="border-l-4 border-l-green-500">
                            <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">Revenus
                                Perçus</h3>
                            <p class="text-3xl font-bold text-gray-900 mt -2">{{ formatCurrency(financialStats.paid_revenue) }}</p>
                            <p class="text-xs text-green-600 mt-1">{{ financialStats.paid_count }} paiements</p>
                        </BaseCard>
                        <BaseCard class="border-l-4 border-l-orange-500">
                            <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">En Attente
                            </h3>
                            <p class="text-3xl font-bold text-gray-900 mt-2">{{ formatCurrency(financialStats.pending_revenue) }}</p>
                            <p class="text-xs text-orange-600 mt-1">{{ financialStats.pending_count }} impayés
                            </p>
                        </BaseCard>
                        <BaseCard class="border-l-4 border-l-blue-500">
                            <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">Revenu Total
                            </h3>
                            <p class="text-3xl font-bold text-gray-900 mt-2">{{ formatCurrency(stats?.total_revenue || 0) }}
                            </p>
                        </BaseCard>
                        <BaseCard class="border-l-4 border-l-purple-500">
                            <h3 class="text-gray-500 text-sm font-medium uppercase tracking-wider">Taux de
                                Paiement</h3>
                            <p class="text-3xl font-bold text-gray-900 mt-2">{{ paymentRate }}%</p>
                        </BaseCard>
                    </div>

                    <!-- Payments List -->
                    <BaseCard>
                        <template #header>
                            <div class="flex justify-between items-center">
                                <h3 class="text-lg font-bold text-gray-900">Suivi des Paiements</h3>
                                <BaseButton variant="secondary" @click="remindUnpaidMembers">
                                    <template #icon>
                                        <Mail :size="18" />
                                    </template>
                                    Relancer les impayés
                                </BaseButton>
                            </div>
                        </template>
                        <div v-if="loadingRegistrations" class="flex justify-center py-20">
                            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue"></div>
                        </div>
                        <div v-else class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Membre</th>
                                        <th
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Catégorie</th>
                                        <th
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Montant</th>
                                        <th
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Statut</th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
                                    <tr v-for="reg in registrations" :key="reg.id" class="hover:bg-gray-50">
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <div class="text-sm font-medium text-gray-900">{{
                                                reg.member.first_name }}
                                                {{
                                                    reg.member.last_name }}</div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <span
                                                class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                                                {{ reg.category.name }}
                                            </span>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                                            {{ reg.category.price }} €
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <div class="flex items-center justify-between">
                                                <div>
                                                    <span v-if="reg.paid"
                                                        class="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                                                        ✓ Payé
                                                    </span>
                                                    <span v-else-if="reg.payment_mode === '3X'"
                                                        class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-100 text-blue-800">
                                                        {{ reg.installments_paid }}/3 Payé
                                                    </span>
                                                    <span v-else
                                                        class="px-2 py-1 text-xs font-semibold rounded-full bg-orange-100 text-orange-800">
                                                        ⏳ En attente
                                                    </span>
                                                </div>
                                                <button @click="openPaymentModal(reg)"
                                                    class="text-gray-400 hover:text-judo-blue ml-2">
                                                    <Edit :size="16" />
                                                </button>
                                            </div>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </BaseCard>
                </div>

                <!-- Registrations Tab -->
                <div v-if="currentTab === 'registrations'">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-bold text-gray-900">Liste des Inscriptions</h2>
                        <BaseButton variant="primary" @click="exportExcel">
                            <template #icon>📄</template>
                            Exporter Excel
                        </BaseButton>
                    </div>

                    <div v-if="loadingRegistrations" class="flex justify-center py-20">
                        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-judo-blue"></div>
                    </div>

                    <BaseCard v-else class="overflow-hidden">
                        <div class="overflow-x-auto">
                            <table class="min-w-full divide-y divide-gray-200">
                                <thead class="bg-gray-50">
                                    <tr>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Enfant</th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Parent</th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Contact</th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Catégorie</th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Prix
                                        </th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Paiement</th>
                                        <th scope="col"
                                            class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                            Statut</th>
                                    </tr>
                                </thead>
                                <tbody class="bg-white divide-y divide-gray-200">
                                    <tr v-for="reg in registrations" :key="reg.id" class="hover:bg-gray-50">
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <div class="text-sm font-medium text-gray-900">{{
                                                reg.member.first_name }}
                                                {{
                                                    reg.member.last_name }}</div>
                                            <div class="text-xs text-gray-500">Né(e) le {{ reg.member.birth_date
                                            }}
                                            </div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <div class="text-sm text-gray-900">{{ reg.member.parent_name ||
                                                'N/A' }}
                                            </div>
                                            <div class="text-xs text-gray-500">{{ reg.member.parent_email ||
                                                'N/A' }}
                                            </div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <div class="text-sm text-gray-900">{{ reg.member.phone || 'N/A' }}
                                            </div>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <span
                                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                                                {{ reg.category.name }}
                                            </span>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                            {{ reg.category.price }} €
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <span v-if="reg.paid"
                                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                                Payé
                                            </span>
                                            <span v-else
                                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                                                Non payé
                                            </span>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap">
                                            <span class="text-sm text-gray-900">{{ reg.status }}</span>
                                        </td>
                                        <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                            <button @click="openPriceModal(reg)"
                                                class="text-judo-blue hover:text-blue-900">
                                                Modifier Tarif
                                            </button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </BaseCard>
                </div>

                <!-- Edit Price Modal -->
                <div v-if="showPriceModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title"
                    role="dialog" aria-modal="true">
                    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                            @click="showPriceModal = false"></div>

                        <span class="hidden sm:inline-block sm:align-middle sm:h-screen"
                            aria-hidden="true">&#8203;</span>

                        <div
                            class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                <div class="sm:flex sm:items-start">
                                    <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
                                        <h3 class="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                                            Modifier le tarif
                                        </h3>
                                        <div class="mt-2">
                                            <p class="text-sm text-gray-500 mb-4">
                                                Appliquer une remise manuelle pour {{
                                                    editingRegistration?.member.first_name }}.
                                            </p>

                                            <div class="space-y-4">
                                                <BaseInput type="number" v-model="priceForm.discount_percentage"
                                                    label="Remise en pourcentage (%)" min="0" max="100" step="0.01" />

                                                <BaseInput type="number" v-model="priceForm.discount_amount"
                                                    label="Remise en euros (€)" min="0" step="0.01" />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                                <BaseButton variant="primary" @click="updatePrice" class="w-full sm:w-auto sm:ml-3">
                                    Enregistrer
                                </BaseButton>
                                <BaseButton variant="white" @click="showPriceModal = false"
                                    class="mt-3 w-full sm:mt-0 sm:w-auto">
                                    Annuler
                                </BaseButton>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Events Tab -->
                <div v-if="currentTab === 'events'">
                    <EventList v-if="!selectedEvent" @manage-convocations="selectEvent" />
                    <ConvocationManager v-else :event="selectedEvent" @back="selectedEvent = null" />
                </div>

                <!-- Attendance Tab -->
                <div v-if="currentTab === 'attendance'">
                    <div class="mb-6 flex space-x-4">
                        <button @click="attendanceSubTab = 'sheets'"
                            class="px-4 py-2 rounded-lg font-medium transition-colors"
                            :class="attendanceSubTab === 'sheets' ? 'bg-judo-blue text-white' : 'bg-white text-gray-600 hover:bg-gray-50'">
                            Feuilles de présence
                        </button>
                        <button @click="attendanceSubTab = 'courses'"
                            class="px-4 py-2 rounded-lg font-medium transition-colors"
                            :class="attendanceSubTab === 'courses' ? 'bg-judo-blue text-white' : 'bg-white text-gray-600 hover:bg-gray-50'">
                            Gestion des Cours
                        </button>
                    </div>

                    <AttendanceSheet v-if="attendanceSubTab === 'sheets'" />
                    <CourseManager v-else />
                </div>

                <!-- Seasons & Categories Tab -->
                <!-- Seasons Tab -->
                <div v-if="currentTab === 'seasons'">
                    <SeasonManager />
                </div>

                <!-- Gallery Tab -->
                <!-- Gallery Tab -->
                <div v-if="currentTab === 'gallery'">
                    <GalleryManager />
                </div>

                <!-- Users Tab -->
                <div v-if="currentTab === 'users'">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-bold text-gray-900">Gestion des Utilisateurs</h2>
                        <BaseButton variant="primary" @click="showUserModal = true">
                            <template #icon>👤</template>
                            Créer un compte Parent
                        </BaseButton>
                    </div>

                    <BaseCard>
                        <div class="p-6 text-center text-gray-500">
                            <p>Utilisez le bouton ci-dessus pour créer manuellement un compte parent.</p>
                            <p class="text-sm mt-2">Le parent pourra ensuite se connecter avec ces identifiants.
                            </p>
                        </div>
                    </BaseCard>
                </div>

                <!-- Create User Modal -->
                <div v-if="showUserModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title"
                    role="dialog" aria-modal="true">
                    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                            @click="showUserModal = false"></div>

                        <span class="hidden sm:inline-block sm:align-middle sm:h-screen"
                            aria-hidden="true">&#8203;</span>

                        <div
                            class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                                    Créer un compte Parent
                                </h3>
                                <form @submit.prevent="createUser" class="space-y-4">
                                    <BaseInput id="new-username" label="Nom d'utilisateur" v-model="userForm.username"
                                        required placeholder="ex: dupont_famille" />
                                    <BaseInput id="new-email" label="Email (Optionnel)" type="email"
                                        v-model="userForm.email" placeholder="ex: contact@famille.com" />
                                    <BaseInput id="new-password" label="Mot de passe" type="password"
                                        v-model="userForm.password" required placeholder="********" />

                                    <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                        <BaseButton type="submit" variant="primary" :loading="loadingUser"
                                            class="w-full sm:col-start-2">
                                            Créer le compte
                                        </BaseButton>
                                        <BaseButton type="button" variant="white" @click="showUserModal = false"
                                            class="mt-3 w-full sm:mt-0 sm:col-start-1">
                                            Annuler
                                        </BaseButton>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Bulk Email Modal -->
                <div v-if="showEmailModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title"
                    role="dialog" aria-modal="true">
                    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                            @click="showEmailModal = false"></div>
                        <span class="hidden sm:inline-block sm:align-middle sm:h-screen"
                            aria-hidden="true">&#8203;</span>
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
                                <form @submit.prevent="sendBulkEmail" class="space-y-4">
                                    <BaseInput id="email-subject" label="Sujet" v-model="emailForm.subject" required
                                        placeholder="Sujet de l'email" />
                                    <div>
                                        <BaseTextarea id="email-body" label="Message" v-model="emailForm.body" rows="6"
                                            required placeholder="Votre message..." />
                                    </div>
                                    <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                        <BaseButton type="submit" variant="primary" :loading="sendingEmail"
                                            class="w-full sm:col-start-2">
                                            Envoyer
                                        </BaseButton>
                                        <BaseButton type="button" variant="white" @click="showEmailModal = false"
                                            class="mt-3 w-full sm:mt-0 sm:col-start-1">
                                            Annuler
                                        </BaseButton>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Edit Member Modal -->
                <div v-if="showEditMemberModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title"
                    role="dialog" aria-modal="true">
                    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                        <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                            @click="showEditMemberModal = false"></div>
                        <span class="hidden sm:inline-block sm:align-middle sm:h-screen"
                            aria-hidden="true">&#8203;</span>

                        <!-- Payment Management Modal -->
                        <div v-if="showPaymentModal" class="fixed inset-0 z-50 overflow-y-auto"
                            aria-labelledby="modal-title" role="dialog" aria-modal="true">
                            <div
                                class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                                <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity"
                                    aria-hidden="true" @click="showPaymentModal = false"></div>
                                <span class="hidden sm:inline-block sm:align-middle sm:h-screen"
                                    aria-hidden="true">&#8203;</span>
                                <div
                                    class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                                            Gérer le paiement
                                        </h3>
                                        <p class="text-sm text-gray-500 mb-4">
                                            Adhérent : {{ editingPaymentReg?.member.first_name }} {{
                                                editingPaymentReg?.member.last_name }}
                                        </p>

                                        <div class="space-y-4">
                                            <div>
                                                <label class="block text-sm font-medium text-gray-700 mb-1">Mode de
                                                    paiement</label>
                                                <div class="flex space-x-4 mt-2">
                                                    <label class="inline-flex items-center">
                                                        <input type="radio" class="form-radio text-judo-blue"
                                                            value="FULL" v-model="paymentForm.payment_mode">
                                                        <span class="ml-2">Comptant</span>
                                                    </label>
                                                    <label class="inline-flex items-center">
                                                        <input type="radio" class="form-radio text-judo-blue" value="3X"
                                                            v-model="paymentForm.payment_mode">
                                                        <span class="ml-2">3 Fois</span>
                                                    </label>
                                                </div>
                                            </div>

                                            <div v-if="paymentForm.payment_mode === '3X'"
                                                class="bg-gray-50 p-4 rounded-lg">
                                                <label class="block text-sm font-medium text-gray-700 mb-2">Suivi des
                                                    mensualités</label>
                                                <div class="space-y-2">
                                                    <label class="flex items-center">
                                                        <input type="checkbox" class="form-checkbox text-judo-blue"
                                                            :checked="paymentForm.installments_paid >= 1"
                                                            @change="updateInstallments(1)">
                                                        <span class="ml-2">1ère mensualité</span>
                                                    </label>
                                                    <label class="flex items-center">
                                                        <input type="checkbox" class="form-checkbox text-judo-blue"
                                                            :checked="paymentForm.installments_paid >= 2"
                                                            @change="updateInstallments(2)">
                                                        <span class="ml-2">2ème mensualité</span>
                                                    </label>
                                                    <label class="flex items-center">
                                                        <input type="checkbox" class="form-checkbox text-judo-blue"
                                                            :checked="paymentForm.installments_paid >= 3"
                                                            @change="updateInstallments(3)">
                                                        <span class="ml-2">3ème mensualité</span>
                                                    </label>
                                                </div>
                                            </div>

                                            <div v-else>
                                                <label class="flex items-center mt-4">
                                                    <input type="checkbox" class="form-checkbox text-judo-blue"
                                                        v-model="paymentForm.paid">
                                                    <span class="ml-2 font-medium">Marquer comme payé</span>
                                                </label>
                                            </div>
                                        </div>

                                        <div
                                            class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                            <BaseButton variant="primary" @click="savePayment" :loading="savingPayment"
                                                class="w-full sm:col-start-2">
                                                Enregistrer
                                            </BaseButton>
                                            <BaseButton variant="white" @click="showPaymentModal = false"
                                                class="mt-3 w-full sm:mt-0 sm:col-start-1">
                                                Annuler
                                            </BaseButton>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div
                            class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
                            <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4" id="modal-title">
                                    Modifier le membre
                                </h3>
                                <form @submit.prevent="updateMember" class="space-y-5">
                                    <div class="grid grid-cols-2 gap-4">
                                        <BaseInput id="edit-firstname" label="Prénom"
                                            v-model="editMemberForm.first_name" required />
                                        <BaseInput id="edit-lastname" label="Nom" v-model="editMemberForm.last_name"
                                            required />
                                    </div>
                                    <BaseInput id="edit-email" label="Email" type="email"
                                        v-model="editMemberForm.email" />
                                    <BaseInput id="edit-phone" label="Téléphone" v-model="editMemberForm.phone" />

                                    <div class="grid grid-cols-2 gap-4">
                                        <BaseInput id="edit-birthdate" label="Date de naissance" type="date"
                                            v-model="editMemberForm.birth_date" required />
                                        <div class="w-full">
                                            <label class="block text-sm font-medium text-gray-700 mb-1">Genre</label>
                                            <div class="flex space-x-4 mt-2">
                                                <label class="inline-flex items-center">
                                                    <input type="radio" class="form-radio text-judo-blue" name="gender"
                                                        value="M" v-model="editMemberForm.gender">
                                                    <span class="ml-2">Masculin</span>
                                                </label>
                                                <label class="inline-flex items-center">
                                                    <input type="radio" class="form-radio text-judo-blue" name="gender"
                                                        value="F" v-model="editMemberForm.gender">
                                                    <span class="ml-2">Féminin</span>
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                    <BaseInput id="edit-license" label="Numéro de licence"
                                        v-model="editMemberForm.license_number" />
                                    <BaseInput id="edit-address" label="Adresse" v-model="editMemberForm.address" />

                                    <div>
                                        <BaseListbox v-model="editMemberForm.weight_category" :options="weightChoices"
                                            label="Catégorie de poids" placeholder="Sélectionner une catégorie..." />
                                    </div>

                                    <div class="mt-5 sm:mt-6 sm:grid sm:grid-cols-2 sm:gap-3 sm:grid-flow-row-dense">
                                        <BaseButton type="submit" variant="primary" :loading="updatingMember"
                                            class="w-full sm:col-start-2">
                                            Enregistrer
                                        </BaseButton>
                                        <BaseButton type="button" variant="white" @click="showEditMemberModal = false"
                                            class="mt-3 w-full sm:mt-0 sm:col-start-1">
                                            Annuler
                                        </BaseButton>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Weigh-in Modal -->
        <div v-if="showWeighInModal" class="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title"
            role="dialog" aria-modal="true">
            <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
                <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" aria-hidden="true"
                    @click="showWeighInModal = false"></div>
                <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
                <div
                    class="inline-block align-bottom bg-white rounded-xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-100">
                    <div class="bg-white px-6 pt-6 pb-6">
                        <div class="flex items-center justify-between mb-6">
                            <h3 class="text-xl font-bold text-gray-900" id="modal-title">
                                Pesée - {{ weighInMember?.first_name }} {{ weighInMember?.last_name }}
                            </h3>
                            <button @click="showWeighInModal = false" class="text-gray-400 hover:text-gray-500">
                                <span class="sr-only">Fermer</span>
                                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>
                        <form @submit.prevent="saveWeight" class="space-y-6">
                            <div>
                                <BaseListbox
                                    v-model="weighInForm.weight_category"
                                    :options="ALL_WEIGHTS"
                                    label="Catégorie de poids"
                                    placeholder="Sélectionner une catégorie..."
                                />
                            </div>

                            <div
                                class="flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-3 space-y-3 space-y-reverse sm:space-y-0">
                                <BaseButton type="button" variant="white" @click="showWeighInModal = false"
                                    class="w-full sm:w-auto">
                                    Annuler
                                </BaseButton>
                                <BaseButton type="submit" variant="primary" :loading="savingWeight"
                                    class="w-full sm:w-auto">
                                    Enregistrer
                                </BaseButton>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/utils/axios'
import {
    Users,
    ClipboardList,
    ClipboardCheck,
    LayoutDashboard,
    Wallet,
    Calendar,
    Settings,
    Image as ImageIcon,
    UserCog,
    LogOut,
    Plus
} from 'lucide-vue-next'
import EventList from '../components/EventList.vue'
import ConvocationManager from '../components/ConvocationManager.vue'
import BaseCard from '../components/ui/BaseCard.vue'
import BaseButton from '../components/ui/BaseButton.vue'
import BaseInput from '../components/ui/BaseInput.vue'
import BaseListbox from '../components/ui/BaseListbox.vue'
import BaseTextarea from '../components/ui/BaseTextarea.vue'
import MembersTable from '../components/admin/MembersTable.vue'
import GalleryManager from '../components/admin/GalleryManager.vue'
import SeasonManager from '../components/admin/SeasonManager.vue'
import DashboardStats from '../components/admin/DashboardStats.vue'
import CourseManager from '../components/admin/CourseManager.vue'
import AttendanceSheet from '../components/admin/AttendanceSheet.vue'
import { useToastStore } from '../stores/toast'



const router = useRouter()
const toast = useToastStore()

// State
const currentTab = ref('dashboard')
const attendanceSubTab = ref('sheets')
const selectedEvent = ref(null)
const stats = ref(null)
const registrations = ref([])
const loading = ref(true)
const loadingRegistrations = ref(false)
const error = ref(null)


// Members state
const allMembers = ref([])
const loadingMembers = ref(false)
const categories = ref([])
const selectedMembers = ref([]) // Used for modal
const showEmailModal = ref(false)
const sendingEmail = ref(false)
const emailForm = ref({
    subject: '',
    body: ''
})

// Edit Member State
const showEditMemberModal = ref(false)
const updatingMember = ref(false)
const editingMemberId = ref(null)
const editMemberForm = ref({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    birth_date: '',
    license_number: '',
    address: '',
    gender: 'M',
    weight_category: ''
})

// Weigh-in State
const showWeighInModal = ref(false)
const savingWeight = ref(false)
const weighInMember = ref(null)
const weighInForm = ref({
    weight_category: ''
})

const openWeighInModal = (member) => {
    weighInMember.value = member
    weighInForm.value = {
        weight_category: member.weight_category || ''
    }
    showWeighInModal.value = true
}

const saveWeight = async () => {
    savingWeight.value = true
    try {
        await api.patch(`/api/members/${weighInMember.value.id}/`, {
            weight_category: weighInForm.value.weight_category
        })
        toast.success('Poids mis à jour')
        showWeighInModal.value = false
        await fetchMembers()
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de la mise à jour du poids")
    } finally {
        savingWeight.value = false
    }
}

import { getWeightCategories, ALL_WEIGHTS } from '@/utils/judo-weights'

const weightChoices = computed(() => {
    // Admins should have access to all weight categories, regardless of age/gender
    return ALL_WEIGHTS
})

// Seasons & Categories state
const seasons = ref([])
const showSeasonModal = ref(false)
const showCategoryModal = ref(false)
const editingCategory = ref(null)
const categoryForm = ref({
    name: '',
    code: '',
    price: 0,
    age_min: 0,
    age_max: 0
})

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false
}

// Computed Data for Charts


// Filtered members


// Financial stats
const financialStats = computed(() => {
    const paid = registrations.value.filter(r => r.paid)
    const pending = registrations.value.filter(r => !r.paid)

    return {
        paid_revenue: paid.reduce((sum, r) => sum + parseFloat(r.category.price || 0), 0),
        paid_count: paid.length,
        pending_revenue: pending.reduce((sum, r) => sum + parseFloat(r.category.price || 0), 0),
        pending_count: pending.length
    }
})

const paymentRate = computed(() => {
    if (registrations.value.length === 0) return 0
    return Math.round((financialStats.value.paid_count / registrations.value.length) * 100)
})





// Methods
const fetchStats = async () => {
    try {
        const res = await api.get('/api/statistics/')
        stats.value = res.data
    } catch (e) {
        console.error(e)
        error.value = "Erreur lors du chargement des statistiques."
    } finally {
        loading.value = false
    }
}

const fetchRegistrations = async () => {
    loadingRegistrations.value = true
    try {
        const res = await api.get('/api/registrations/')
        registrations.value = res.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des inscriptions")
    } finally {
        loadingRegistrations.value = false
    }
}

const fetchMembers = async () => {
    loadingMembers.value = true
    try {
        const res = await api.get('/api/members/')
        allMembers.value = res.data
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors du chargement des membres")
    } finally {
        loadingMembers.value = false
    }
}

const fetchCategories = async () => {
    try {
        const res = await api.get('/api/categories/')
        categories.value = res.data
    } catch (e) {
        console.error(e)
    }
}

const getMemberCategory = (memberId) => {
    const reg = registrations.value.find(r => r.member.id === memberId)
    return reg ? reg.category.name : 'N/A'
}

const isMemberActive = (memberId) => {
    return registrations.value.some(r => r.member.id === memberId && r.status === 'VALIDATED')
}



const selectEvent = (event) => {
    selectedEvent.value = event
}

const exportExcel = async () => {
    try {
        const response = await api.get('/api/registrations/export/', {
            responseType: 'blob', // Important for file download
        })

        // Create download link
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `inscriptions_${new Date().toISOString().slice(0, 10)}.xlsx`)
        document.body.appendChild(link)
        link.click()
        link.remove()
    } catch (e) {
        console.error("Erreur export excel", e)
        alert("Erreur lors de l'export")
    }
}

// Edit Price Modal
const showPriceModal = ref(false)
const editingRegistration = ref(null)
const priceForm = ref({
    discount_percentage: 0,
    discount_amount: 0
})

const openPriceModal = (reg) => {
    editingRegistration.value = reg
    priceForm.value = {
        discount_percentage: reg.discount_percentage || 0,
        discount_amount: reg.discount_amount || 0
    }
    showPriceModal.value = true
}

const updatePrice = async () => {
    if (!editingRegistration.value) return

    try {
        await api.patch(`/api/registrations/${editingRegistration.value.id}/`, {
            discount_percentage: priceForm.value.discount_percentage,
            discount_amount: priceForm.value.discount_amount
        })

        // Refresh list

        showPriceModal.value = false
        editingRegistration.value = null
        toast.success("Tarif mis à jour avec succès")
    } catch (e) {
        console.error("Erreur update price", e)
        toast.error("Erreur lors de la mise à jour du tarif")
    }
}

// Payment Management
const showPaymentModal = ref(false)
const editingPaymentReg = ref(null)
const savingPayment = ref(false)
const paymentForm = ref({
    payment_mode: 'FULL',
    installments_paid: 0,
    paid: false
})

const openPaymentModal = (reg) => {
    editingPaymentReg.value = reg
    paymentForm.value = {
        payment_mode: reg.payment_mode || 'FULL',
        installments_paid: reg.installments_paid || 0,
        paid: reg.paid
    }
    showPaymentModal.value = true
}

const updateInstallments = (level) => {
    // Logic: if checking level 2, implies level 1 is paid.
    // If unchecking level 2 (and was 3), becomes 1.
    // Simplified: just set the value based on click, but let's be smart.
    // Actually, simple radio-like behavior for checkboxes or just direct set is easier.
    // Let's just toggle. If clicking 2 and current is 1, set to 2. If clicking 2 and current is 2, set to 1.
    // Better yet: just set to the level if checked, or level-1 if unchecked.
    // But user might click out of order. Let's just trust the highest checked.
    // Re-implementation:
    if (paymentForm.value.installments_paid >= level) {
        paymentForm.value.installments_paid = level - 1
    } else {
        paymentForm.value.installments_paid = level
    }
}

const savePayment = async () => {
    if (!editingPaymentReg.value) return
    savingPayment.value = true

    // Auto-calculate paid status
    let isPaid = paymentForm.value.paid
    if (paymentForm.value.payment_mode === '3X') {
        isPaid = paymentForm.value.installments_paid >= 3
    }

    try {
        await api.patch(`/api/registrations/${editingPaymentReg.value.id}/`, {
            payment_mode: paymentForm.value.payment_mode,
            installments_paid: paymentForm.value.installments_paid,
            paid: isPaid
        })
        toast.success("Paiement mis à jour")
        showPaymentModal.value = false
        await fetchRegistrations()
        await fetchStats() // Refresh stats too
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de la mise à jour du paiement")
    } finally {
        savingPayment.value = false
    }
}

const remindUnpaidMembers = () => {
    const unpaidRegs = registrations.value.filter(r => !r.paid)
    if (unpaidRegs.length === 0) {
        toast.info("Aucun impayé à relancer")
        return
    }
    const unpaidMemberIds = unpaidRegs.map(r => r.member.id)
    selectedMembers.value = unpaidMemberIds
    
    // Pre-fill email
    emailForm.value = {
        subject: "Rappel de cotisation - Judo Club",
        body: "Bonjour,\n\nSauf erreur de notre part, nous n'avons pas encore reçu le règlement de votre cotisation pour la saison en cours.\n\nMerci de régulariser votre situation rapidement.\n\nCordialement,\nLe Bureau"
    }
    showEmailModal.value = true
}

const formatCurrency = (value) => {
    const number = parseFloat(value)
    if (isNaN(number)) return '0,00 €'
    return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' }).format(number)
}

// User Creation Logic
const showUserModal = ref(false)
const userForm = ref({
    username: '',
    email: '',
    password: ''
})
const loadingUser = ref(false)

const createUser = async () => {
    loadingUser.value = true
    try {
        await api.post('/api/register/', userForm.value)
        toast.success(`Compte parent "${userForm.value.username}" créé avec succès !`)
        showUserModal.value = false
        userForm.value = { username: '', email: '', password: '' }
    } catch (e) {
        console.error(e)
        // Error handling is done globally but we can add specific feedback here if needed
    } finally {
        loadingUser.value = false
    }
}

const handleBulkEmailAction = (memberIds) => {
    selectedMembers.value = memberIds
    openEmailModal()
}

const openEmailModal = () => {
    emailForm.value = { subject: '', body: '' }
    showEmailModal.value = true
}

const getRecipientPreview = () => {
    if (selectedMembers.value.length === 0) return ''
    const firstFew = selectedMembers.value.slice(0, 3).map(id => {
        const member = allMembers.value.find(m => m.id === id)
        return member ? `${member.first_name} ${member.last_name}` : 'Inconnu'
    })
    const remaining = selectedMembers.value.length - 3
    if (remaining > 0) {
        return `${firstFew.join(', ')} et ${remaining} autres...`
    }
    return firstFew.join(', ')
}

const sendBulkEmail = async () => {
    sendingEmail.value = true
    try {
        await api.post('/api/emails/bulk-send/', {
            member_ids: selectedMembers.value,
            subject: emailForm.value.subject,
            body: emailForm.value.body
        })
        toast.success('Emails envoyés avec succès')
        showEmailModal.value = false
        selectedMembers.value = []
    } catch (e) {
        console.error(e)
        toast.error("Erreur lors de l'envoi des emails")
    } finally {
        sendingEmail.value = false
    }
}

const openEditMemberModal = (member) => {
    editingMemberId.value = member.id
    editMemberForm.value = {
        first_name: member.first_name,
        last_name: member.last_name,
        email: member.email,
        phone: member.phone,
        birth_date: member.birth_date,
        license_number: member.license_number,
        address: member.address,
        gender: member.gender,
        weight_category: member.weight_category || ''
    }
    showEditMemberModal.value = true
}

const updateMember = async () => {
    updatingMember.value = true
    console.log("Updating member", editingMemberId.value, "with data:", editMemberForm.value)
    try {
        await api.patch(`/api/members/${editingMemberId.value}/`, editMemberForm.value)
        toast.success('Membre mis à jour avec succès')
        showEditMemberModal.value = false
        // Refresh members list
        await fetchMembers()
    } catch (e) {
        console.error("Error updating member:", e)
        toast.error("Erreur lors de la mise à jour du membre")
    } finally {
        updatingMember.value = false
    }
}

const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('username')
    localStorage.removeItem('is_staff')
    router.push('/login')
}

watch(currentTab, (newTab) => {
    if (newTab === 'registrations' && registrations.value.length === 0) {
        fetchRegistrations()
    }
    if (newTab === 'members' && allMembers.value.length === 0) {
        fetchMembers()
    }
    // Members tab filters rely on registrations data
    if (newTab === 'members' && registrations.value.length === 0) {
        fetchRegistrations()
    }
    if (newTab === 'finances' && registrations.value.length === 0) {
        fetchRegistrations()
    }

})

onMounted(() => {
    fetchStats()
    fetchCategories()
})
</script>
