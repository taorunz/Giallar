Require Import Reals.
Require Import Psatz.

(**********************)
(** Unitary Programs **)
(**********************)
Inductive qgate : Set :=
  | skip : qgate
  | gX : nat -> qgate
  | gY : nat -> qgate
  | gZ : nat -> qgate
  | gH : nat -> qgate
  | gCNOT (cn0 cn1 : nat) (Hneq : cn0 <> cn1): qgate
  | gSWAP (cn0 cn1 : nat) (Hneq : cn0 <> cn1): qgate
.
Inductive qcirc : Set :=
| seq :  qcirc -> qgate  -> qcirc 
| empty : qcirc
.

Notation "p1 ; p2" := (seq p1 p2) (at level 50).

Check empty; skip; gX 1.

Require Import Setoid.
Require Export QWIRE.Quantum.
Require Export QWIRE.Proportional.

Definition pad {n} (start dim : nat) (A : Square (2^n)) : Square (2^dim) :=
  if start + n <=? dim then I (2^start) ⊗ A ⊗ I (2^(dim - (start + n))) else Zero.

Lemma WF_pad : forall n start dim (A : Square (2^n)),
  WF_Matrix A ->
  WF_Matrix (pad start dim A).
Proof.
  intros n start dim A WFA. unfold pad.
  bdestruct (start + n <=? dim); auto with wf_db.
Qed.  

Definition eval_X (dim n : nat) : Square (2^dim) :=
 @pad 1 n dim (σx)
.

Definition eval_Y (dim n : nat) : Square (2^dim) :=
 @pad 1 n dim (σy)
.

Definition eval_Z (dim n : nat) : Square (2^dim) :=
 @pad 1 n dim (σz)
.

Definition eval_H (dim n : nat) : Square (2^dim) :=
 @pad 1 n dim (hadamard)
.

(* Restriction: m <> n and m, n < dim *)
Definition eval_cnot (dim m n: nat) : Square (2^dim) :=
  if (m <? n) then
    @pad (1+(n-m-1)+1) m dim (∣1⟩⟨1∣ ⊗ I (2^(n-m-1)) ⊗ σx .+ ∣0⟩⟨0∣ ⊗ I (2^(n-m-1)) ⊗ I 2)
  else if (n <? m) then
    @pad (1+(m-n-1)+1) n dim (σx ⊗ I (2^(m-n-1)) ⊗ ∣1⟩⟨1∣ .+ I 2 ⊗ I (2^(m-n-1)) ⊗ ∣0⟩⟨0∣)
  else
    Zero.

Definition eval_swap (dim m n: nat) : Square (2^dim) :=
  if (m <? n) then
      @pad (1+(n-m-1)+1) m dim 
             ( ∣0⟩⟨0∣ ⊗ I (2^(n-m-1)) ⊗ ∣0⟩⟨0∣ .+
               ∣0⟩⟨1∣ ⊗ I (2^(n-m-1)) ⊗ ∣1⟩⟨0∣ .+
               ∣1⟩⟨0∣ ⊗ I (2^(n-m-1)) ⊗ ∣0⟩⟨1∣ .+
               ∣1⟩⟨1∣ ⊗ I (2^(n-m-1)) ⊗ ∣1⟩⟨1∣ )
  else if (n <? m) then
      @pad (1+(m-n-1)+1) n dim 
             ( ∣0⟩⟨0∣ ⊗ I (2^(m-n-1)) ⊗ ∣0⟩⟨0∣ .+
               ∣0⟩⟨1∣ ⊗ I (2^(m-n-1)) ⊗ ∣1⟩⟨0∣ .+
               ∣1⟩⟨0∣ ⊗ I (2^(m-n-1)) ⊗ ∣0⟩⟨1∣ .+
               ∣1⟩⟨1∣ ⊗ I (2^(m-n-1)) ⊗ ∣1⟩⟨1∣ )
  else
      Zero.

Lemma WF_eval_x : forall dim n, WF_Matrix (eval_X dim n).
Proof.
  intros. apply WF_pad. rewrite <- pauli_x_rotation. apply WF_rotation.
Qed.  

Lemma WF_eval_y : forall dim n, WF_Matrix (eval_Y dim n).
Proof.
  intros. apply WF_pad. rewrite <- pauli_y_rotation. apply WF_rotation.
Qed.  

Lemma WF_eval_z : forall dim n, WF_Matrix (eval_Z dim n).
Proof.
  intros. apply WF_pad. rewrite <- pauli_z_rotation. apply WF_rotation.
Qed.  

Lemma WF_eval_h : forall dim n, WF_Matrix (eval_H dim n).
Proof.
  intros. apply WF_pad. rewrite <- hadamard_rotation. apply WF_rotation.
Qed.  
  
Lemma WF_eval_cnot : forall dim m n, WF_Matrix (eval_cnot dim m n). 
Proof.
  intros dim m n.
  unfold eval_cnot.
  bdestruct (m <? n); [|bdestruct (n <? m)]; 
    try apply WF_pad;
    unify_pows_two; auto with wf_db.
Qed.  

Lemma WF_eval_swap : forall dim m n, WF_Matrix (eval_swap dim m n).
Proof.
  intros. unfold eval_swap. 
  bdestruct (m <? n); [|bdestruct (n <? m)]; 
   gridify; try apply WF_pad;
  try replace (2^(S(d+1)))%nat with (2* 2^d * 2)%nat;
  repeat apply WF_plus; auto with wf_db.
Qed.

Definition eval_gate dim (c : qgate) : Matrix (2^dim) (2^dim) :=
    match c with
    | skip    => I (2^dim)
    | gX n    => eval_X dim n
    | gY n    => eval_Y dim n
    | gZ n    => eval_Z dim n
    | gH n    => eval_H dim n
    | gCNOT m n _ => eval_cnot dim m n
    | gSWAP m n _ => eval_swap dim m n
end.

Fixpoint eval dim (c : qcirc) : Matrix (2^dim) (2^dim) :=
    match c with
    | empty    => I (2^dim)
    | c1 ; c2 => eval dim c1 × eval_gate dim c2 
end.

Theorem WF_eval :
    forall c dim, WF_Matrix (eval dim c).
Proof.
  induction c; intros; simpl in *.
  - apply WF_mult. apply IHc. destruct q; simpl.
    + apply WF_I.
    + apply WF_eval_x.
    + apply WF_eval_y.
    + apply WF_eval_z.
    + apply WF_eval_h.
    + apply WF_eval_cnot.
    + apply WF_eval_swap.
  - apply WF_I.
Qed.


