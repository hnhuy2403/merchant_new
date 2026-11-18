# ViettelPay Pro – Introduction for Visa

**Prepared by:** Viettel Digital Financial Services (VDF)
**Purpose:** Introduce the ViettelPay Pro app to Visa as a second candidate for Visa Accept SDK integration, alongside Tendoo
**Status:** Draft for discussion – figures marked [TBC] are to be confirmed by VDF

---

## 1. Summary

ViettelPay Pro is the mobile app that Viettel's distribution channel uses to sell digital financial services to end customers. Users are not consumers. They are Viettel's agents, retail points of sale, sales collaborators, field staff and channel managers across Vietnam, many of them in rural and suburban areas.

Through the app, a point of sale can top up mobile phones, sell scratch cards and game cards, collect bills (electricity, water, internet/TV, loan instalments, insurance, school fees, toll top-ups), send and pay out cash transfers, deposit cash into bank accounts and wallets, onboard Viettel Money customers, and accept QR payments.

Today the app does not accept international cards. Integrating Visa Accept would let these points of sale take contactless Visa payments on their own Android phones, with no POS terminal. This would serve customers who prefer to pay by card, and tourists in particular.

| Item | Description |
|---|---|
| App name | ViettelPay Pro (agent/merchant app of the Viettel Money ecosystem) |
| Publisher | Viettel Digital Services / VDF (Viettel Group) |
| Platforms | Android and iOS, free on Google Play and App Store |
| Users | Viettel agents (3 tiers), retail points of sale, sales collaborators (CTV), postal/field staff, channel managers, store tellers |
| Network size | [TBC: number of active points of sale, monthly active users, provinces covered] |
| Transaction volume | [TBC: monthly transactions and value] |
| Device profile | [TBC: share of Android devices, share with NFC] |
| Consumer counterpart | Viettel Money (formerly ViettelPay) – the consumer wallet app |

## 2. Role of ViettelPay Pro in the Viettel Money ecosystem

Viettel Money serves consumers. ViettelPay Pro serves the people who serve them in person: it is the "assisted" channel. Customers who don't use a wallet themselves, or who need cash in or cash out, go to a nearby Viettel point of sale. The point of sale completes the transaction for them in ViettelPay Pro, and the customer pays in cash.

```
 End customer (cash, QR, soon cards)
          │
          ▼
 Point of sale / agent using ViettelPay Pro
          │  pays from its prefunded float account
          ▼
 Viettel platform (Bankplus / BCCS / Viettel Money)
          │
          ▼
 Billers, telcos, banks, schools, insurers, transport, ...
```

## 3. Who uses the app

| User type | Who they are | How they sign in | How transactions are settled |
|---|---|---|---|
| Agents, tiers 1/2/3 | Businesses distributing Viettel services. Tier 1 is managed by Viettel; tiers 2 and 3 are sub-agents created by the tier above | Agent code + PIN + OTP | Debited from the agent's prefunded float account |
| Point of sale | Shops and retailers (grocery, phone shops, etc.) | Point-of-sale code + PIN + OTP | Debited from the float account |
| Postal / construction staff, account managers | Viettel group staff selling services in the field | Staff user + PIN + OTP | Debited from the float account |
| Sales collaborators (CTV) / household businesses | Individual freelance sellers | Collaborator user + PIN + OTP | Telecom sales recorded as receivables; other services debited from the float account |
| Channel managers | Viettel staff managing points of sale | Manager user + PIN + OTP | Telecom sales recorded as receivables; other services debited from the float account |
| Store tellers | Staff at Viettel stores | Teller user + PIN + OTP | Recorded as receivables for the user |

**Agent hierarchy.** Agents work in three tiers. A parent agent can create sub-agents in the app, reset their PINs, move float to them, and set their commission and fee rates. When a sub-agent makes a sale, the system calculates and pays commission to every tier at once.

## 4. Account and funds model

Each user has a **prefunded float account** in Viettel's system. Most services are paid out of this balance:

- **Fund in:** from the user's linked bank account or Viettel Money account, or from a channel manager who collects cash and tops up the float on the user's behalf (the receiving user confirms the top-up).
- **Fund out:** withdrawal to the linked bank account or wallet.
- **Transfers between agents:** a parent moves float to a sub-agent, and the sub-agent returns it.
- **Visibility:** available balance, total balance, monthly cash flow (used to calculate commission tiers), and full balance history.
- **Earnings:** the channel earns commission on telecom products and a sales fee on bill payment, transfer and financial services. Both are visible in reports inside the app.

This model matters for card acceptance: the point of sale already holds a settlement account inside Viettel, which is a natural place to receive the proceeds of card payments.

## 5. Services available today

| Group | Services |
|---|---|
| Telecom | Mobile top-up for all Vietnamese networks (Viettel, Vinaphone, Mobifone, Vietnamobile, Gmobile); Viettel postpaid bill payment; scratch cards for all networks; game cards (Garena, Zing, Vcoin, Funtap, Gate, etc.); Viettel and partner internet, TV and fixed-line bills; debt collection for terminated Viettel contracts |
| Bill payment | Electricity (EVN); water (many regional providers); consumer loan instalments (Home Credit, FE Credit, Mcredit, OCB Credit, Shinhan Finance, etc.); insurance sales (Bao Viet, Prudential, MB Ageas, etc.); school fees; VETC electronic toll top-up; train tickets |
| Cash and money transfer | Domestic cash transfer (receiver collects at a Viettel counter or gets cash delivered at home); cash pay-out to receivers; deposits to any bank account by card number or account number; deposits to MB / Viettel Money accounts by phone number; Viettel Money top-up |
| Customer onboarding | Identity verification (eKYC) of Viettel Money customers, including at the customer's home: the collaborator captures ID documents and confirms with the customer's OTP |
| Field task management | Managers assign cash-delivery and home-onboarding jobs to collaborators. Collaborators accept or reject them, get cash advances, and explain overdue jobs. Every step is tracked with deadlines and SMS alerts |
| QR acceptance | Each point of sale has its own static QR ("MyQR"). Customers scan it with the Viettel Money or Bankplus app to pay for goods; the point of sale sees QR revenue and history in the app |

## 6. Platform capabilities relevant to Visa Accept

| Capability | What exists today | Relevance to Visa Accept |
|---|---|---|
| Merchant identity | Every point of sale is a registered entity in Viettel's channel system (BCCS), with a manager, location and linked phone number | Starting data for merchant onboarding and KYB |
| Authentication | Sign-in with code + PIN + OTP; fingerprint sign-in; PIN confirmation for every transaction | Strong user authentication before payment acceptance |
| Settlement account | Prefunded float account, plus a linked bank or wallet account | Where card proceeds can be settled |
| Transaction history | Search by date, service and status (success, failed, timeout); reprint receipts | Card transactions can appear in the same history |
| Reversal | Voids with customer OTP, or with district manager approval, within set time windows | A pattern to reuse for card refunds and voids |
| Reconciliation | Daily transaction file sent by email; commission and fee reports | Card reconciliation can use the same channel |
| Risk controls | Duplicate-transaction warning; per-user service blocking; transaction limits | A base for card fraud and limit controls |
| Field network and supervision | Managers and district directors oversee points of sale, assign tasks and receive SMS alerts | Merchant activation, training and monitoring at scale |
| Customer support | In-app tutorials, video guides, hotline and the assigned manager's contact details | Merchant support for the new card feature |

## 7. Why ViettelPay Pro for Visa Accept

1. **Reach beyond cities and tourist hubs.** The ViettelPay Pro network reaches small shops nationwide, including places where POS terminals are rare.
2. **Merchants are already active and verified.** Points of sale already use the app every day for financial transactions, have a settlement account, and have a Viettel manager. Card acceptance is a new feature in an app they know, not a new product to adopt.
3. **Assisted channel for card users.** Customers, including international visitors, can pay for top-ups, bills and goods by tapping a Visa card or phone at the point of sale instead of paying cash.
4. **Fits with Tendoo.** Tendoo serves household businesses through a sales and management app. ViettelPay Pro serves Viettel's distribution and service-point network. Together they cover both merchant segments with one Visa Accept integration approach run by VDF.

## 8. Proposed integration scope (for discussion)

- **Tap to Phone:** embed the Visa Accept SDK in the Android version of ViettelPay Pro so eligible points of sale can accept contactless cards on NFC phones.
- **Use cases:** (a) the customer pays for goods at the shop; (b) the customer pays for a ViettelPay Pro service (top-up, bill payment) by card instead of cash [subject to Visa rules and VDF policy].
- **Onboarding:** reuse existing point-of-sale data for KYB; activate the feature per point of sale, starting with a pilot group.
- **Settlement:** card proceeds settle to the point of sale's account via VDF / Viettel Money.
- **Operations:** card transactions in the app's history and reports; refunds following the existing reversal pattern; reconciliation through the existing daily file.

## 9. Points to confirm with Visa

- Eligibility of ViettelPay Pro user types (agents, shops, individual collaborators) for Visa Accept.
- KYB requirements, and whether existing channel data is sufficient.
- Whether cards can pay for services sold through the app (top-ups, bill payments).
- Transaction and monthly limits, pricing (MDR) and incentive programmes, as discussed for Tendoo.
- SDK requirements: Android versions, NFC, attestation, and certification steps.

---

*Source: ViettelPay Pro user guide (QT.VDS.SP.08, revised 2021–2022) and public app store information. Some service lists and screens may have changed in the current app version.*
