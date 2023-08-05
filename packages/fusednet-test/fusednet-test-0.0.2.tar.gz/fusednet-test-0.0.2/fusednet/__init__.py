
def test_on_syth_fiber():

    import matplotlib.pyplot as plt
    from sklearn.datasets import make_blobs
    import numpy as np
    from numpy import linalg as LA
    import tensorflow as tf
    data, label = make_blobs(n_samples=200, n_features=2, centers=1, random_state=123)
    # plt.figure(figsize=[8,8])
    # plt.plot(data[:,0], data[:,1], ".")

    heads=[]
    tails=[]
    centers=np.hstack([data,np.zeros((200,1))])



    #--------------------------dilations
    dilafacmat=np.random.uniform(low=0.5, high=1.5, size=[1,2])
    dilation=np.append(dilafacmat,[[1]],axis=1)
    centerscp=centers*dilation
    heads=np.copy(centerscp)

    dilafacmat=np.random.uniform(low=0.5, high=1.5, size=[1,2])
    dilation=np.append(dilafacmat,[[1]],axis=1)
    centerscp=centers*dilation
    tails=np.copy(centerscp)

    #--------------------------dilations
    heads[:,2]=heads[:,2]+10
    tails[:,2]=tails[:,2]-10


    # heads[:,2]=centers[:,2]+5
    # tails[:,2]=centers[:,2]-5

    fibsSythLong=np.hstack([heads.flatten()[:,None],centers.flatten()[:,None],tails.flatten()[:,None]])
    preturb=np.random.normal(loc=0, scale=0.1, size=fibsSythLong.shape)
    fibsSythLong=fibsSythLong+preturb
    fibsSythLongComplete=fibsSythLong.reshape((200,3,3))
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # for fibs in fibsSythLongComplete:
    #     tfib=np.transpose(fibs)
    #     ax.plot3D(tfib[:,0],tfib[:,1],tfib[:,2],'orange')


    #---------------------------------2nd dataset-----------------------------------------------
    data, label = make_blobs(n_samples=200, n_features=2, centers=1, random_state=123)
    # plt.figure(figsize=[8,8])
    # plt.plot(data[:,0], data[:,1], ".")

    heads=[]
    tails=[]
    centers=np.hstack([data,np.zeros((200,1))])
    #displacement of the first data set
    centers[:,0]=centers[:,0]+10
    centers[:,1]=centers[:,1]+10
    # centers[:,0]=centers[:,0]+3
    # centers[:,1]=centers[:,1]+3
    #------------------------------
    #--------------------------dilations
    dilafacmat=np.random.uniform(low=0.5, high=1.5, size=[1,2])
    dilation=np.append(dilafacmat,[[1]],axis=1)
    centerscp=centers*dilation
    heads=np.copy(centerscp)

    dilafacmat=np.random.uniform(low=0.5, high=1.5, size=[1,2])
    dilation=np.append(dilafacmat,[[1]],axis=1)
    centerscp=centers*dilation
    tails=np.copy(centerscp)

    #--------------------------dilations
    heads[:,2]=heads[:,2]+10
    tails[:,2]=tails[:,2]-10

    fibsSythLong=np.hstack([heads.flatten()[:,None],centers.flatten()[:,None],tails.flatten()[:,None]])
    preturb=np.random.normal(loc=0, scale=0.1, size=fibsSythLong.shape)
    fibsSythLong=fibsSythLong+preturb
    fibsSythLongComplete_2=fibsSythLong.reshape((200,3,3))
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # for fibs in fibsSythLongComplete:
    #     tfib=np.transpose(fibs)
    #     ax.plot3D(tfib[:,0],tfib[:,1],tfib[:,2],'orange')

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax = plt.axes(projection='3d')
    for fibs in fibsSythLongComplete:
        tfib=np.transpose(fibs)
        ax.plot3D(tfib[:,0],tfib[:,1],tfib[:,2],'orange')


    for fibs in fibsSythLongComplete_2:
        tfib = np.transpose(fibs)
        ax.plot3D(tfib[:, 0], tfib[:, 1], tfib[:, 2], 'blue')
    plt.show()

    totalsythfib=np.append(fibsSythLongComplete,fibsSythLongComplete_2,axis=0)
    totalsythfib.tofile("sythnfibsshiftymuscle.FIB")



    fibsOnBall = []
    fibsCenterandLength = []
    formatLength=3
    for fib in fibsSythLongComplete:
        L = np.asmatrix(fib)
        #This transpose is not always necessary, as long as the format is [x1,x2;y1,y2;z1,z2...]
    #   L = np.transpose(L)
        ctr = np.sum(L, axis=1) / formatLength
        L = L - ctr
        lgth = LA.norm(L)
        L=L/LA.norm(L)
        L_=np.array(L)

    #visualization
        # fig = plt.figure()
        # ax = plt.axes(projection="3d")
        # ax.plot3D(L_[0, :], L_[1, :], L_[2, :], 'orange')
        # plt.show()


        A=1-LA.norm(L[:,0])**2
        L_S_m=L[:,1:]*A**(-1/2)
    #   print(LA.norm(L_S_m))
        fibOnBall=np.array(L_S_m.flatten())
        fibsOnBall.append(fibOnBall)
        c = np.squeeze(np.asarray(ctr))
        fibCenterandLength = np.hstack((c, lgth))
        fibsCenterandLength.append(fibCenterandLength)


    for fib in fibsSythLongComplete_2:
        L = np.asmatrix(fib)
        #This transpose is not always necessary, as long as the format is [x1,x2;y1,y2;z1,z2...]
    #   L = np.transpose(L)
        ctr = np.sum(L, axis=1) / formatLength
        L = L - ctr
        lgth = LA.norm(L)
        L=L/LA.norm(L)
        L_=np.array(L)

    #visualization
        # fig = plt.figure()
        # ax = plt.axes(projection="3d")
        # ax.plot3D(L_[0, :], L_[1, :], L_[2, :], 'orange')
        # plt.show()


        A=1-LA.norm(L[:,0])**2
        L_S_m=L[:,1:]*A**(-1/2)
    #   print(LA.norm(L_S_m))
        fibOnBall=np.array(L_S_m.flatten())
        fibsOnBall.append(fibOnBall)
        c = np.squeeze(np.asarray(ctr))
        fibCenterandLength = np.hstack((c, lgth))
        fibsCenterandLength.append(fibCenterandLength)


    np.asarray(fibsOnBall).tofile("sythnfibsshiftymuscle" + ".bbb")
    np.asarray(fibsCenterandLength).tofile("sythnfibsshiftymusle" + ".CtaL")





    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = ""
    import matplotlib.pyplot as plt
    from tensorflow import keras
    from tensorflow.python.keras.layers import concatenate
    import tensorflow as tf

    # def cluster_sythetic_fibers(pathfibs,pathctal)

    syth1fibs=np.fromfile('E:\GeneralSoftware\Pythonprojects\Research\Auto-encoder\Ver3.0\sythnfibsshiftymuscle.bbb')
    syth1ctal=np.fromfile('E:\GeneralSoftware\Pythonprojects\Research\Auto-encoder\Ver3.0\sythnfibsshiftymusle.CtaL')
    syth1ctalr=syth1ctal.reshape(400,4)
    syth1fibsr=syth1fibs.reshape(400,6)


    y=syth1fibsr
    num_classes=4
    Centers_Lengths_dimension=4
    fibs_input_dim=6
    recon_dim=fibs_input_dim
    inputs_center_and_length = tf.keras.Input(shape=(Centers_Lengths_dimension,))
    inputs_fibs_on_ball = tf.keras.Input(shape=(fibs_input_dim,))

    encoding_dim = 3
    encoder = keras.layers.Dense(encoding_dim, activation='tanh')(inputs_fibs_on_ball)
    encoder=keras.Model(inputs=inputs_fibs_on_ball, outputs=encoder)
    decoder=keras.layers.Dense(recon_dim,activation='linear')(encoder.outputs[0])
    decoder=keras.Model(inputs=encoder.inputs, outputs=decoder)

    estimator=keras.layers.Dense(20, activation='tanh')(concatenate([encoder.outputs[0],inputs_center_and_length ],axis=1))

    estimator=keras.layers.Dense(num_classes,activation='softmax')(estimator)
    #estimator=keras.Model(inputs=encoder.inputs, outputs=estimator)
    estimator=keras.Model(inputs=[encoder.inputs,inputs_center_and_length], outputs=estimator)
    #concatenate output of the two :

    combined = concatenate([decoder.output, estimator.output,encoder.output,inputs_center_and_length,],axis=1)
    fusednet = keras.Model(inputs=[inputs_center_and_length,inputs_fibs_on_ball],outputs=combined)


    learningrate,lambda1,lambda2=0.001,1e-1,1e-6
    epochs=3000
    batch_size=128


    def my_EnergyLoss_fn(y_true, y_pred):
        gamma = y_pred[:, recon_dim:recon_dim + num_classes]
        z = y_pred[:, recon_dim + num_classes:]
        gamma_sum = tf.reduce_sum(gamma, axis=0)
        phi = tf.reduce_mean(gamma, axis=0)
        mu = tf.einsum('ik,il->kl', gamma, z) / gamma_sum[:, None]
        z_centered = tf.sqrt(gamma[:, :, None]) * (z[:, None, :] - mu[None, :, :])
        sigma = tf.einsum(
                'ikl,ikm->klm', z_centered, z_centered) / gamma_sum[:, None, None]

        # Calculate a cholesky decomposition of covariance in advance
        n_features = z.shape[1]
        min_vals = tf.linalg.diag(tf.ones(n_features, dtype=tf.float32)) * 1e-6
        L = tf.linalg.cholesky(sigma + min_vals[None, :, :])

        z_centered = z[:, None, :] - mu[None, :, :]
        v = tf.linalg.triangular_solve(L, tf.transpose(z_centered, [1, 2, 0]))

        log_det_sigma = 2.0 * tf.reduce_sum(tf.math.log(tf.linalg.diag_part(L)), axis=1)
        d = z.shape[1]
        logits = tf.math.log(phi[:, None]) - 0.5 * (tf.reduce_sum(tf.square(v), axis=1)
                                                        + d * tf.math.log(2.0 * np.pi)
                                                        + log_det_sigma[:, None])
        energies = - tf.reduce_logsumexp(logits, axis=0)
        enerloss = tf.reduce_mean(energies)
        return enerloss
    def my_ReconLoss_fn(y_true, y_pred):
        recon = y_pred[:, 0:recon_dim]
        input = y_true[:, 0:recon_dim]
        Zr = tf.math.reduce_sum(tf.reduce_mean(tf.square(recon - input), axis=-1))  # +cce(probvec, Label)
        return Zr
    def my_PenaultyLoss_fn(y_true, y_pred):
        gamma = y_pred[:, recon_dim:recon_dim + num_classes]
        z = y_pred[:, recon_dim + num_classes:]
        gamma_sum = tf.reduce_sum(gamma, axis=0)
        phi = tf.reduce_mean(gamma, axis=0)
        mu = tf.einsum('ik,il->kl', gamma, z) / gamma_sum[:, None]
        z_centered = tf.sqrt(gamma[:, :, None]) * (z[:, None, :] - mu[None, :, :])
        sigma = tf.einsum(
                'ikl,ikm->klm', z_centered, z_centered) / gamma_sum[:, None, None]
        diag_loss = tf.reduce_sum(tf.divide(1, tf.linalg.diag_part(sigma)))
        return diag_loss
    def my_totalLoss_fn(y_true, y_pred):
        return   my_ReconLoss_fn(y_true,y_pred)+lambda1*my_EnergyLoss_fn(y_true,y_pred)+lambda2*my_PenaultyLoss_fn(y_true,y_pred)
    def my_active_classes(y_true, y_pred):
        gamma = y_pred[:, recon_dim:recon_dim + num_classes]
        z = y_pred[:, recon_dim + num_classes:]
        indexes = tf.math.argmax(gamma, axis=1)
        y,idx=tf.unique(indexes)
        print(y)
        print(y.shape)
        print(tf.size(y))
        numactiveclasses=tf.size(y)
        return numactiveclasses

    es=EarlyStopping(monitor='val_my_totalLoss_fn', mode='min',verbose=0, patience=50)
    fusednet.compile(optimizer='adam', loss=my_totalLoss_fn,run_eagerly=False,metrics=[my_totalLoss_fn, my_ReconLoss_fn,my_EnergyLoss_fn,my_PenaultyLoss_fn,my_active_classes])
    keras.utils.plot_model(fusednet, show_shapes=True) #This command give us model plot.

    history=fusednet.fit([syth1ctalr,syth1fibsr], y, batch_size=batch_size, epochs=epochs, validation_split=0.3,callbacks=[es])

    postdata=fusednet.predict([syth1ctalr,syth1fibsr])
    fig, axs = plt.subplots(3, 2,figsize=(15,15))
    axs[0, 0].plot(history.history['my_totalLoss_fn'])
    axs[0, 0].set_title('Total_Loss')
    axs[0, 1].plot(history.history['my_ReconLoss_fn'])
    axs[0, 1].set_title('Reconstruction Loss')
    axs[1, 0].plot(history.history['my_EnergyLoss_fn'])
    axs[1, 0].set_title('Energy_Loss')
    axs[1, 1].plot(history.history['my_PenaultyLoss_fn'])
    axs[1, 1].set_title('Penaulty_Loss')
    axs[2, 0].plot(history.history['my_active_classes'])
    axs[2, 0].set_title('Active_classes')

    def plot_at_y(arr, val, **kwargs):
        plt.plot(arr, np.zeros_like(arr) + val, 'x', **kwargs)
        plt.show()

    recon = postdata[:, 0:recon_dim]
    gamma = postdata[:, recon_dim:recon_dim + num_classes]
    indexes=tf.math.argmax(gamma,axis=1)
    activeclasses=np.unique(indexes)
    index=[]
    for cl in activeclasses:
        index.append(tf.where(indexes==cl).numpy())
    for inds in index:
        axs[2, 1].plot(inds, np.zeros_like(inds) + 0, 'x')

    plt.show()


    colorstring='bgrc'
    totalfibsagain=np.fromfile("sythnfibsshiftymuscle.FIB")
    totalfibsagain=totalfibsagain.reshape((400,3,3))
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax = plt.axes(projection='3d')
    for i in range(0,len(index)):


        for fibs in totalfibsagain[np.squeeze(index[i])]:
            tfib=np.transpose(fibs)
            ax.plot3D(tfib[:,0],tfib[:,1],tfib[:,2],color=colorstring[i])
    plt.show()

    return 0