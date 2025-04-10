from gym.spaces import Box

from ftr_algo.algorithms.rl.ddpg import DDPG
from ftr_algo.algorithms.rl.ppo import PPO
from ftr_algo.algorithms.rl.sac import SAC
from ftr_algo.algorithms.rl.td3 import TD3
from ftr_algo.algorithms.rl.trpo import TRPO


def process_sarl(args, env, cfg_train, logdir):
    learn_cfg = cfg_train["learn"]
    is_testing = learn_cfg["test"]
    # is_testing = True
    # Override resume and testing flags if they are passed as parameters.
    if args.model_dir != "":
        is_testing = True
        chkpt_path = args.model_dir

    if args.max_iterations != -1:
        cfg_train["learn"]["max_iterations"] = args.max_iterations

    # logdir = logdir + "_seed{}".format(env.task.cfg["seed"])

    """Set up the algo system for training or inferencing."""
    model = eval(args.algo.upper())(
        vec_env=env,
        cfg_train=cfg_train,
        device=env.rl_device,
        sampler=learn_cfg.get("sampler", "sequential"),
        log_dir=logdir,
        is_testing=is_testing,
        print_log=learn_cfg["print_log"],
        apply_reset=False,
        asymmetric=(env.state_space.shape[0] > 0 if isinstance(env.state_space, Box) else False),
    )

    # ppo.test("/home/hp-3070/logs/demo/scissors/ppo_seed0/model_6000.pt")
    if is_testing and args.model_dir != "":
        print("Loading model from {}".format(chkpt_path))
        model.test(chkpt_path)
    elif args.model_dir != "":
        print("Loading model from {}".format(chkpt_path))
        model.load(chkpt_path)

    return model
