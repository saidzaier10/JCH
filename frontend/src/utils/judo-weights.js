// Official FFJDA 2024-2025 Weight Categories

export const WEIGHT_CATEGORIES = {
    'EVEIL': [ // 4-5 ans (Mixte)
        { value: '-20', label: '-20 kg' }, { value: '-23', label: '-23 kg' }, { value: '-26', label: '-26 kg' },
        { value: '-29', label: '-29 kg' }, { value: '+29', label: '+29 kg' }
    ],
    'MINI_POUSSINS': [ // 6-7 ans (Mixte)
        { value: '-20', label: '-20 kg' }, { value: '-23', label: '-23 kg' }, { value: '-26', label: '-26 kg' },
        { value: '-29', label: '-29 kg' }, { value: '-32', label: '-32 kg' }, { value: '-35', label: '-35 kg' },
        { value: '-38', label: '-38 kg' }, { value: '-42', label: '-42 kg' }, { value: '-46', label: '-46 kg' },
        { value: '+46', label: '+46 kg' }
    ],
    'POUSSINS': [ // 8-9 ans (Mixte)
        { value: '-20', label: '-20 kg' }, { value: '-23', label: '-23 kg' }, { value: '-26', label: '-26 kg' },
        { value: '-29', label: '-29 kg' }, { value: '-32', label: '-32 kg' }, { value: '-34', label: '-34 kg' },
        { value: '-38', label: '-38 kg' }, { value: '-42', label: '-42 kg' }, { value: '-46', label: '-46 kg' },
        { value: '+46', label: '+46 kg' }
    ],
    'BENJAMINS': { // 10-11 ans
        'M': [
            { value: '-26', label: '-26 kg' }, { value: '-30', label: '-30 kg' }, { value: '-34', label: '-34 kg' },
            { value: '-38', label: '-38 kg' }, { value: '-42', label: '-42 kg' }, { value: '-46', label: '-46 kg' },
            { value: '-50', label: '-50 kg' }, { value: '-55', label: '-55 kg' }, { value: '-60', label: '-60 kg' },
            { value: '-66', label: '-66 kg' }, { value: '+66', label: '+66 kg' }
        ],
        'F': [
            { value: '-28', label: '-28 kg' }, { value: '-32', label: '-32 kg' }, { value: '-36', label: '-36 kg' },
            { value: '-40', label: '-40 kg' }, { value: '-44', label: '-44 kg' }, { value: '-48', label: '-48 kg' },
            { value: '-52', label: '-52 kg' }, { value: '-57', label: '-57 kg' }, { value: '-63', label: '-63 kg' },
            { value: '+63', label: '+63 kg' }
        ]
    },
    'MINIMES': { // 12-13 ans
        'M': [
            { value: '-34', label: '-34 kg' }, { value: '-38', label: '-38 kg' }, { value: '-42', label: '-42 kg' },
            { value: '-46', label: '-46 kg' }, { value: '-50', label: '-50 kg' }, { value: '-55', label: '-55 kg' },
            { value: '-60', label: '-60 kg' }, { value: '-66', label: '-66 kg' }, { value: '-73', label: '-73 kg' },
            { value: '+73', label: '+73 kg' }
        ],
        'F': [
            { value: '-36', label: '-36 kg' }, { value: '-40', label: '-40 kg' }, { value: '-44', label: '-44 kg' },
            { value: '-48', label: '-48 kg' }, { value: '-52', label: '-52 kg' }, { value: '-57', label: '-57 kg' },
            { value: '-63', label: '-63 kg' }, { value: '-70', label: '-70 kg' }, { value: '+70', label: '+70 kg' }
        ]
    },
    'CADETS': { // 14-16 ans
        'M': [
            { value: '-46', label: '-46 kg' }, { value: '-50', label: '-50 kg' }, { value: '-55', label: '-55 kg' },
            { value: '-60', label: '-60 kg' }, { value: '-66', label: '-66 kg' }, { value: '-73', label: '-73 kg' },
            { value: '-81', label: '-81 kg' }, { value: '-90', label: '-90 kg' }, { value: '+90', label: '+90 kg' }
        ],
        'F': [
            { value: '-40', label: '-40 kg' }, { value: '-44', label: '-44 kg' }, { value: '-48', label: '-48 kg' },
            { value: '-52', label: '-52 kg' }, { value: '-57', label: '-57 kg' }, { value: '-63', label: '-63 kg' },
            { value: '-70', label: '-70 kg' }, { value: '+70', label: '+70 kg' }
        ]
    },
    'JUNIORS_SENIORS': { // 17+ ans
        'M': [
            { value: '-60', label: '-60 kg' }, { value: '-66', label: '-66 kg' }, { value: '-73', label: '-73 kg' },
            { value: '-81', label: '-81 kg' }, { value: '-90', label: '-90 kg' }, { value: '-100', label: '-100 kg' },
            { value: '+100', label: '+100 kg' }
        ],
        'F': [
            { value: '-48', label: '-48 kg' }, { value: '-52', label: '-52 kg' }, { value: '-57', label: '-57 kg' },
            { value: '-63', label: '-63 kg' }, { value: '-70', label: '-70 kg' }, { value: '-78', label: '-78 kg' },
            { value: '+78', label: '+78 kg' }
        ]
    }
}

export const ALL_WEIGHTS = [
    { value: '-20', label: '-20 kg' }, { value: '-23', label: '-23 kg' }, { value: '-26', label: '-26 kg' },
    { value: '-28', label: '-28 kg' }, { value: '-29', label: '-29 kg' }, { value: '-30', label: '-30 kg' },
    { value: '-32', label: '-32 kg' }, { value: '-34', label: '-34 kg' }, { value: '-35', label: '-35 kg' },
    { value: '-36', label: '-36 kg' }, { value: '-38', label: '-38 kg' }, { value: '-40', label: '-40 kg' },
    { value: '-42', label: '-42 kg' }, { value: '-44', label: '-44 kg' }, { value: '-46', label: '-46 kg' },
    { value: '-48', label: '-48 kg' }, { value: '-50', label: '-50 kg' }, { value: '-52', label: '-52 kg' },
    { value: '-55', label: '-55 kg' }, { value: '-57', label: '-57 kg' }, { value: '-60', label: '-60 kg' },
    { value: '-63', label: '-63 kg' }, { value: '-66', label: '-66 kg' }, { value: '-70', label: '-70 kg' },
    { value: '-73', label: '-73 kg' }, { value: '-78', label: '-78 kg' }, { value: '-81', label: '-81 kg' },
    { value: '-90', label: '-90 kg' }, { value: '-100', label: '-100 kg' }, { value: '+29', label: '+29 kg' },
    { value: '+46', label: '+46 kg' }, { value: '+63', label: '+63 kg' }, { value: '+66', label: '+66 kg' },
    { value: '+70', label: '+70 kg' }, { value: '+73', label: '+73 kg' }, { value: '+78', label: '+78 kg' },
    { value: '+90', label: '+90 kg' }, { value: '+100', label: '+100 kg' }
]

export const getWeightCategories = (birthDateString, gender) => {
    if (!birthDateString) return ALL_WEIGHTS

    const birthDate = new Date(birthDateString)
    const today = new Date()
    let age = today.getFullYear() - birthDate.getFullYear()

    let categoryWeights = null

    if (age <= 5) categoryWeights = WEIGHT_CATEGORIES.EVEIL
    else if (age <= 7) categoryWeights = WEIGHT_CATEGORIES.MINI_POUSSINS
    else if (age <= 9) categoryWeights = WEIGHT_CATEGORIES.POUSSINS
    else if (age <= 11) categoryWeights = WEIGHT_CATEGORIES.BENJAMINS
    else if (age <= 13) categoryWeights = WEIGHT_CATEGORIES.MINIMES
    else if (age <= 16) categoryWeights = WEIGHT_CATEGORIES.CADETS
    else categoryWeights = WEIGHT_CATEGORIES.JUNIORS_SENIORS

    // Handle gender specific categories
    if (categoryWeights && !Array.isArray(categoryWeights)) {
        return categoryWeights[gender] || ALL_WEIGHTS
    }

    return categoryWeights || ALL_WEIGHTS
}
