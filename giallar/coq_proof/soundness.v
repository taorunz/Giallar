Require Import certiq.

Inductive symbqubit : Set :=
| qbase : symbqubit
| qX :  symbqubit -> symbqubit
| qY :  symbqubit -> symbqubit
| qZ :  symbqubit -> symbqubit
| qH :  symbqubit -> symbqubit
| qCNOT_1 : nat -> symbqubit -> symbqubit
| qCNOT_2 : nat -> symbqubit -> symbqubit
| qSWAP_1 : nat -> symbqubit -> symbqubit
| qSWAP_2 : nat -> symbqubit -> symbqubit
.

Definition map := nat -> symbqubit.
Definition map_get  (n : nat) (m : map) : symbqubit := m n.
Definition map_set  (n :nat) (q : symbqubit) (m : map) : map :=
fun n' => if Nat.eq_dec n n' then q else m n'.


Definition map_set2 (n1 : nat) (q1 : symbqubit) (n2 : nat) (q2 : symbqubit) (m : map): map := 
  map_set n1 q1 (map_set n2 q2 m).

Definition symbeval_gate (c : qgate) (input : map): map :=
    match c with
    | skip    => input
    | gX n    => map_set n (qX (map_get n input)) input
    | gY n    => map_set n (qY (map_get n input)) input
    | gZ n    => map_set n (qZ (map_get n input)) input
    | gH n    => map_set n (qH (map_get n input)) input
    | gCNOT n1 n2 _  => map_set2 n1 (qCNOT_1 n2 (map_get n1 input)) n2 (qCNOT_2 n1 (map_get n2 input)) input
    | gSWAP n1 n2 _  => map_set2 n1 (qSWAP_1 n2 (map_get n1 input)) n2 (qSWAP_2 n1 (map_get n2 input)) input
end.

Fixpoint symbeval (c : qcirc) (input : map): map :=
    match c with
    | empty    => input
    | c1 ; c2 => symbeval_gate c2 (symbeval c1 input)
end.



Fixpoint calc_symb (c : qcirc) (dim : nat) (qm : map) (m : Matrix (2^dim) (2^dim)) : option (Matrix (2^dim) (2^dim)) :=
  match c with
  | empty => Some m
  | c' ; g => match g with
              | skip => calc_symb c' dim qm m
              | gX n => match map_get n qm with 
                        | qX q => match calc_symb c' dim (map_set n q qm) m with 
                                  | Some m' => Some (m' × (eval_X dim n))
                                  | _ => None
                                  end
                        | _ => None
                        end
              | gY n => match map_get n qm with 
                        | qY q => match calc_symb c' dim (map_set n q qm) m with 
                                  | Some m' => Some (m' × (eval_Y dim n))
                                  | _ => None
                                  end
                        | _ => None
                        end
              | gZ n => match map_get n qm with 
                        | qZ q => match calc_symb c' dim (map_set n q qm) m with 
                                  | Some m' => Some (m' × (eval_Z dim n))
                                  | _ => None
                                  end
                        | _ => None
                        end
              | gH n => match map_get n qm with 
                        | qH q => match calc_symb c' dim (map_set n q qm) m with 
                                  | Some m' => Some (m' × (eval_H dim n))
                                  | _ => None
                                  end
                        | _ => None
                        end
              | gCNOT n1 n2 _=> match map_get n1 qm, map_get n2 qm with 
                              | qCNOT_1 n2' q1, qCNOT_2 n1' q2 =>
                                match Nat.eq_dec n1 n1', Nat.eq_dec n2 n2', calc_symb c' dim (map_set2 n1 q1 n2 q2 qm) m with 
                                | in_left, in_left, Some m' => Some (m' × (eval_cnot dim n1 n2))
                                | _, _, _ => None
                                end 
                              | _, _ => None
                              end
              | gSWAP n1 n2 _=> match map_get n1 qm, map_get n2 qm with 
                              | qSWAP_1 n2' q1, qSWAP_2 n1' q2 =>
                                match Nat.eq_dec n1 n1', Nat.eq_dec n2 n2', calc_symb c' dim (map_set2 n1 q1 n2 q2 qm) m with 
                                | in_left, in_left, Some m' => Some (m' × (eval_swap dim n1 n2))
                                | _, _, _ => None
                                end 
                              | _, _ => None
                              end
              end
end.

(* map lemmas *)
Lemma map_gss : forall n q m, map_get n (map_set n q m) = q.
Proof.
  intros. unfold map_get, map_set. destruct (Nat.eq_dec n n); easy.
Qed.

Lemma map_s2s : forall n q1 q2 m, map_set n q1 (map_set n q2 m) = map_set n q1 m.
Proof.
  intros. apply functional_extensionality. intros.
  unfold map_get, map_set. destruct (Nat.eq_dec n x); easy.
Qed.

Definition map_sgs : forall n m, map_set n (map_get n m) m = m.
Proof.
  intros. apply functional_extensionality. intros.
  unfold map_get, map_set. destruct (Nat.eq_dec n x); auto.
Qed.

Definition map_gsd : forall n0 n1 q m, n0 <> n1 -> map_get n0 (map_set n1 q m) = map_get n0 m.
Proof.
  intros. unfold map_get, map_set. destruct (Nat.eq_dec n1 n0); auto. congruence.
Qed.

Definition map_ssd : forall n0 n1 q0 q1 m, n0 <> n1 -> map_set n0 q0 (map_set n1 q1 m) = map_set n1 q1 (map_set n0 q0 m).
Proof.
  intros. apply functional_extensionality. intros.
  unfold map_get, map_set. destruct (Nat.eq_dec n0 x); try easy.
  destruct (Nat.eq_dec n1 x); try easy. congruence.
Qed.

Lemma calc_symb_valid :
  forall (c : qcirc) (dim : nat) (input : map) (m : Matrix (2^dim) (2^dim)),
  exists m',
         calc_symb c dim (symbeval c input) m = Some m'.
Proof.
  induction c; intros; simpl in *.
  - destruct q; simpl.
    + destruct (IHc dim input m) as [m' Heq]. rewrite Heq. esplit. reflexivity.
    + rewrite map_gss. rewrite map_s2s. rewrite map_sgs.
      destruct (IHc dim input m) as [m' Heq]. rewrite Heq. esplit. reflexivity.
    + rewrite map_gss. rewrite map_s2s. rewrite map_sgs.
      destruct (IHc dim input m) as [m' Heq]. rewrite Heq. esplit. reflexivity.
    + rewrite map_gss. rewrite map_s2s. rewrite map_sgs.
      destruct (IHc dim input m) as [m' Heq]. rewrite Heq. esplit. reflexivity.
    + rewrite map_gss. rewrite map_s2s. rewrite map_sgs.
      destruct (IHc dim input m) as [m' Heq]. rewrite Heq. esplit. reflexivity.
    + unfold map_set2. rewrite map_gss. rewrite map_gsd. rewrite map_gss. 
      rewrite map_ssd. rewrite map_s2s. rewrite map_ssd. rewrite map_s2s.
      destruct (Nat.eq_dec cn0 cn0). destruct (Nat.eq_dec cn1 cn1).
      repeat rewrite map_sgs.
      destruct (IHc dim input m) as [m' Heq]. rewrite Heq. esplit. reflexivity.

      elim n. reflexivity.
      elim n. reflexivity.
      intro Hfalse. elim Hneq. congruence.
      assumption. 
      intro Hfalse. elim Hneq. congruence.
    + unfold map_set2. rewrite map_gss. rewrite map_gsd. rewrite map_gss. 
      rewrite map_ssd. rewrite map_s2s. rewrite map_ssd. rewrite map_s2s.
      destruct (Nat.eq_dec cn0 cn0). destruct (Nat.eq_dec cn1 cn1).
      repeat rewrite map_sgs.
      destruct (IHc dim input m) as [m' Heq]. rewrite Heq. esplit. reflexivity.

      elim n. reflexivity.
      elim n. reflexivity.
      intro Hfalse. elim Hneq. congruence.
      assumption. 
      intro Hfalse. elim Hneq. congruence.
  - repeat esplit.
Qed.

Lemma aux_symb_eval_soundness :
  forall (c : qcirc) (dim : nat) (qm : map) (m m' : Matrix (2^dim) (2^dim))
        (aux_pre : calc_symb c dim qm m = Some m') (HmWF : WF_Matrix m),
        m' = (m × (eval dim c)).
Proof.
  induction c; intros; simpl in *.
  - destruct q; simpl.
    + apply IHc in aux_pre. rewrite aux_pre. simpl. rewrite Mmult_1_r. reflexivity. apply WF_eval. assumption.
    + destruct (map_get n qm) eqn:Hmn; inversion aux_pre. 
      destruct (calc_symb c dim (map_set n s qm) m) eqn: Hc; inversion aux_pre.
      apply IHc in Hc. rewrite Hc. rewrite Mmult_assoc. reflexivity. assumption.
    + destruct (map_get n qm) eqn:Hmn; inversion aux_pre. 
      destruct (calc_symb c dim (map_set n s qm) m) eqn: Hc; inversion aux_pre.
      apply IHc in Hc. rewrite Hc. rewrite Mmult_assoc. reflexivity. assumption.
    + destruct (map_get n qm) eqn:Hmn; inversion aux_pre. 
      destruct (calc_symb c dim (map_set n s qm) m) eqn: Hc; inversion aux_pre.
      apply IHc in Hc. rewrite Hc. rewrite Mmult_assoc. reflexivity. assumption.
    + destruct (map_get n qm) eqn:Hmn; inversion aux_pre. 
      destruct (calc_symb c dim (map_set n s qm) m) eqn: Hc; inversion aux_pre.
      apply IHc in Hc. rewrite Hc. rewrite Mmult_assoc. reflexivity. assumption.
    + destruct (map_get cn0 qm) eqn:Hmn; inversion aux_pre.
      destruct (map_get cn1 qm) eqn:Hmn0; inversion aux_pre.
      destruct (Nat.eq_dec cn0 n0); inversion aux_pre.
      destruct (Nat.eq_dec cn1 n); inversion aux_pre.
      destruct (calc_symb c dim (map_set2 cn0 s cn1 s0 qm) m) eqn: Hc; inversion aux_pre.
      apply IHc in Hc. rewrite Hc. rewrite Mmult_assoc. reflexivity. assumption.
    + destruct (map_get cn0 qm) eqn:Hmn; inversion aux_pre.
      destruct (map_get cn1 qm) eqn:Hmn0; inversion aux_pre.
      destruct (Nat.eq_dec cn0 n0); inversion aux_pre.
      destruct (Nat.eq_dec cn1 n); inversion aux_pre.
      destruct (calc_symb c dim (map_set2 cn0 s cn1 s0 qm) m) eqn: Hc; inversion aux_pre.
      apply IHc in Hc. rewrite Hc. rewrite Mmult_assoc. reflexivity. assumption.
  - rewrite Mmult_1_r. inversion aux_pre. congruence. assumption.
Qed.

Theorem symb_eval_soundness_weak :
  forall (c : qcirc) (dim : nat) (qm : map) (m' : Matrix (2^dim) (2^dim))
        (aux_pre : calc_symb c dim qm (I (2^dim)) = Some m'),
        m' = eval dim c.
Proof.
  intros. 
  assert (eval dim c = (I (2 ^ dim)) × (eval dim c)) as HI.
    { rewrite Mmult_1_l. reflexivity. apply WF_eval. }
  rewrite HI.
  eapply aux_symb_eval_soundness. eassumption.
  apply WF_I.
Qed.

Theorem symb_eval_soundness :
  forall (c : qcirc) (dim : nat) (input : map),
      exists m',
        calc_symb c dim (symbeval c input) (I (2^dim)) = Some m' /\
        m' = eval dim c.
Proof.
  intros. destruct (calc_symb_valid c dim input (I (2^dim))) as [m Hcal].
  rewrite Hcal. apply symb_eval_soundness_weak in Hcal. rewrite <- Hcal. repeat esplit.
Qed.
