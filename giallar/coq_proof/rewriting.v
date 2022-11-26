Require Import certiq.

Lemma Hneq_mk : forall m k, (m < k)%nat -> (m <> k)%nat.
Proof. intros. intro Hfalse. lia. Qed.

Theorem cnot_cancel :
    forall n m k (Hkn : (S k <= n)%nat) (Hmk : (m < k)%nat),
    eval n (empty; gCNOT m k (Hneq_mk m k Hmk); gCNOT m k (Hneq_mk m k Hmk)) = eval n empty.
Proof.
    intros.
    simpl. unfold eval_cnot. simpl. unfold pad. gridify. Qsimpl.
    repeat rewrite <- kron_plus_distr_r.
    repeat rewrite <- kron_plus_distr_l. Qsimpl.
    repeat rewrite id_kron. 
    replace (2 ^ m * 2 * 2 ^ x * 2 * 2 ^ d0)%nat with (2 ^ m * (2 ^ (x + 1) + (2 ^ (x + 1) + 0)) * 2 ^ d0)%nat.
    reflexivity. rewrite plus_0_r. rewrite Nat.pow_add_r. simpl. lia.
Qed.

Definition build_vector (dim n2 : nat) (inputl : Vector (2^n2)) (inputr : Vector (2^(dim-n2-1))) : Vector (2^dim) :=
    (inputl ⊗ ∣0⟩ ⊗ inputr).

Lemma kron_mixed_product' : forall (m n n' o p q q' r mp nq or: nat)
    (A : Matrix m n) (B : Matrix p q) (C : Matrix n' o) (D : Matrix q' r),
    n = n' -> q = q' ->    
    (mp = m * p)%nat -> (nq = n * q)%nat -> (or = o * r)%nat ->
  (@Mmult mp nq or (@kron m n p q A B) (@kron n' o q' r C D)) =
  (@kron m o p r (@Mmult m n o A C) (@Mmult p q r B D)).
Proof. intros. subst. apply kron_mixed_product. Qed.

Lemma pow_2_2_x : forall (x:nat),
  (2 * 2 ^ x = 2 ^ (x + 1))%nat.
Proof.
  intros. rewrite Nat.pow_add_r.
  simpl. ring.
Qed.

Theorem cnot_bridge_with_ancilla :
        forall dim n1 n2 n3 (inputl : Vector (2^n2)) (inputr : Vector (2^(dim-n2-1))) (Hneq12 : (n1 <> n2)%nat) (Hneq23 : (n2 <> n3)%nat) (Hneq13 : (n1 <> n3)%nat),
            (S n1 <= dim)%nat -> (S n2 <= dim)%nat -> (S n3 <= dim)%nat ->
            (n1 < n2)%nat -> (n2 < n3)%nat ->
            eval dim (empty; gCNOT n1 n2 Hneq12; gCNOT n2 n3 Hneq23; gCNOT n1 n2 Hneq12) × (build_vector dim n2 inputl inputr) = 
            eval dim (empty; gCNOT n1 n3 Hneq13) × (build_vector dim n2 inputl inputr).
Proof.
    intros. simpl. unfold eval_cnot, pad. gridify. Qsimpl. 
    remember (I (2 ^ n1) ⊗ (∣1⟩ × (∣0⟩) †) ⊗ I (2 ^ x0)) as sl0.
    remember (I (2 ^ n1) ⊗ (∣1⟩ × (∣1⟩) †) ⊗ I (2 ^ x0)) as sl1.
    repeat rewrite kron_assoc.
    remember (I (2 ^ x) ⊗ (σx ⊗ I (2 ^ d4))) as srx.
    remember (I (2 ^ x) ⊗ (I 2 ⊗ I (2 ^ d4))) as sri.
    repeat rewrite <- kron_assoc. unfold build_vector. gridify.
    repeat rewrite kron_mixed_product'; try lia.
    replace (∣0⟩ × (∣0⟩) † × ∣0⟩) with ∣0⟩ by solve_matrix.
    replace (∣1⟩ × (∣1⟩) † × ∣0⟩) with (@Zero 2%nat 1%nat) by solve_matrix.
    Qsimpl. reflexivity.
    all: repeat ring_simplify.
    all: try rewrite pow_2_2_x.
    all: replace 4%nat with (2^2)%nat by reflexivity. 
    all: repeat rewrite <- Nat.pow_add_r.
    all: match goal with
          | [|- (2 ^ ?A)%nat = (2 ^ ?B)%nat] => replace A with B
    end; try lia.
Qed.

Theorem x_cancel :
      forall n m (Hnm : (S m <= n)%nat),
      eval n (empty; gX m; gX m) = eval n empty.
Proof.
  intros. simpl. unfold eval_X. unfold pad. gridify.
  replace (σx × σx) with (I 2). reflexivity.
  solve_matrix. 
Qed.

Theorem z_cancel :
      forall n m (Hnm : (S m <= n)%nat),
      eval n (empty; gZ m; gZ m) = eval n empty.
Proof.
  intros. simpl. unfold eval_Z. unfold pad. gridify.
  replace (σz × σz) with (I 2). reflexivity.
  solve_matrix.
Qed. 

Theorem h_cancel :
      forall n m (Hnm : (S m <= n)%nat),
      eval n (empty; gH m; gH m) = eval n empty.
Proof.
  intros. simpl. unfold eval_H. unfold pad. gridify.
  replace (hadamard × hadamard) with (I 2). reflexivity.
  solve_matrix.
Qed.      
  
Theorem cnot_x_commute :
  forall n m k (Hnm : (S m <= n)%nat) (Hnk : (S k <= n)%nat) (Hneq : (m <> k)%nat),
    eval n (empty; gX k; gCNOT m k Hneq) = eval n (empty; gCNOT m k Hneq; gX k).
Proof.
  intros. simpl. unfold eval_X, eval_cnot, pad. gridify; reflexivity.
Qed.

Theorem cnot_z_commute :
  forall n m k (Hnm : (S m <= n)%nat) (Hnk : (S k <= n)%nat) (Hneq : (m <> k)%nat),
    eval n (empty; gZ m; gCNOT m k Hneq) = eval n (empty; gCNOT m k Hneq; gZ m).
Proof.
  intros. simpl. unfold eval_Z, eval_cnot, pad. gridify;
  replace (σz × ∣1⟩⟨1∣) with (∣1⟩⟨1∣ × σz) by solve_matrix;
  replace (σz × ∣0⟩⟨0∣) with (∣0⟩⟨0∣ × σz) by solve_matrix;
  reflexivity.
Qed.

Theorem cnot_commute_sharing_target : 
  forall dim n1 n2 n3 (Hneq12 : (n1 <> n2)%nat) (Hneq13 : (n1 <> n3)%nat),
  (S n1 <= dim)%nat -> (S n2 <= dim)%nat -> (S n3 <= dim)%nat ->
  eval dim (empty; gCNOT n1 n2 Hneq12; gCNOT n1 n3 Hneq13) = eval dim (empty; gCNOT n1 n3 Hneq13; gCNOT n1 n2 Hneq12).
Proof.
  intros. simpl. unfold eval_cnot, pad. 
  gridify; Qsimpl; try reflexivity. (* 8 cases, slow *)
Qed.

Theorem cnot_commute_sharing_control : 
  forall dim n1 n2 n3 (Hneq13 : (n1 <> n3)%nat) (Hneq23 : (n2 <> n3)%nat),
  (S n1 <= dim)%nat -> (S n2 <= dim)%nat -> (S n3 <= dim)%nat ->
  eval dim (empty; gCNOT n1 n3 Hneq13; gCNOT n2 n3 Hneq23) = eval dim (empty; gCNOT n2 n3 Hneq23; gCNOT n1 n3 Hneq13).
Proof.
  intros. simpl. unfold eval_cnot, pad.
  gridify; Qsimpl; try reflexivity. (* 8 cases, slow *)
Qed.

Theorem cnot_bridge :
  forall dim n1 n2 n3 (Hneq12 : (n1 <> n2)%nat) (Hneq23 : (n2 <> n3)%nat) (Hneq13 : (n1 <> n3)%nat),
  (S n1 <= dim)%nat -> (S n2 <= dim)%nat -> (S n3 <= dim)%nat ->
  eval dim (empty; gCNOT n1 n2 Hneq12; gCNOT n2 n3 Hneq23; gCNOT n1 n2 Hneq12; gCNOT n2 n3 Hneq23) = 
  eval dim (empty; gCNOT n1 n3 Hneq13).
Proof.
  intros. simpl. unfold eval_cnot, pad. 
  gridify; Qsimpl. (* very slow *)
  all:repeat rewrite <- kron_plus_distr_r;
  repeat rewrite <- kron_plus_distr_l; Qsimpl; try reflexivity.
  all:repeat rewrite <- kron_plus_distr_r;
      repeat rewrite <- kron_plus_distr_l; Qsimpl; try reflexivity.
Qed.

Theorem swap_cancel :
    forall n m k (Hkn : (S k <= n)%nat) (Hmk : (m < k)%nat),
    eval n (empty; gSWAP m k (Hneq_mk m k Hmk); gSWAP m k (Hneq_mk m k Hmk)) = eval n empty.
Proof.
  intros. simpl. unfold eval_swap, pad. gridify. Qsimpl.
  repeat rewrite <- kron_plus_distr_r.
  repeat rewrite <- kron_plus_distr_l.
  rewrite Mplus_assoc. repeat rewrite <- kron_plus_distr_r.
    repeat rewrite <- kron_plus_distr_l.
  replace (∣0⟩⟨0∣ .+ ∣1⟩⟨1∣) with (I 2) by solve_matrix. reflexivity.
Qed.