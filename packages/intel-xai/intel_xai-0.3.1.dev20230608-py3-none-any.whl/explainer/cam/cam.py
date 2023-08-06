class XGradCAM:
    def __init__(self, model, targetLayer, targetClass, image, dims, device):

        # set any frozen layers to trainable
        # gradcam cannot be calculated without it
        for param in model.parameters():
            if not param.requires_grad:
                param.requires_grad = True

        self.model = model
        self.targetLayer = targetLayer
        self.targetClass = targetClass
        self.image = image
        self.dims = dims
        self.device = device

    def visualize(self):
        from pytorch_grad_cam import XGradCAM, GuidedBackpropReLUModel
        from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
        from pytorch_grad_cam.utils.image import show_cam_on_image, deprocess_image, preprocess_image
        import torch
        import cv2
        import numpy as np
        import matplotlib.pyplot as plt

        self.model.eval().to(self.device)

        image = cv2.resize(self.image, self.dims)
        # convert to rgb if image is grayscale
        converted = False
        if len(image.shape) == 2:
            converted = True 
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        
        rgb_img = np.float32(image) / 255
        input_tensor = preprocess_image(rgb_img,
                                        mean=[0.485, 0.456, 0.406],
                                        std=[0.229, 0.224, 0.225])
        input_tensor = input_tensor.to(self.device)
        
        self.targetLayer = [self.targetLayer]
        
        if self.targetClass is None:
            targets = None
        else:
            targets = [ClassifierOutputTarget(self.targetClass)]

        cam = XGradCAM(self.model, self.targetLayer, use_cuda=torch.cuda.is_available())

        # convert back to grayscale if that is the initial dim
        if converted:
            input_tensor = input_tensor[:, 0:1, :, :]

        grayscale_cam = cam(input_tensor=input_tensor, targets=targets, aug_smooth=False,
                            eigen_smooth=False)
        grayscale_cam = grayscale_cam[0, :]
        cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)
        cam_image = cv2.cvtColor(cam_image, cv2.COLOR_RGB2BGR)

        gb_model = GuidedBackpropReLUModel(model=self.model, use_cuda=torch.cuda.is_available())
        gb = gb_model(input_tensor, target_category=None)
        cam_mask = cv2.merge([grayscale_cam, grayscale_cam, grayscale_cam])
        cam_gb = deprocess_image(cam_mask * gb)
        gb = deprocess_image(gb)

        fig = plt.figure(figsize=(10, 7))
        rows = 1
        columns = 3

        fig.add_subplot(rows, columns, 1)
        plt.imshow(cv2.cvtColor(cam_image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("XGradCAM")

        fig.add_subplot(rows, columns, 2)
        plt.imshow(cv2.cvtColor(gb, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Guided backpropagation")

        fig.add_subplot(rows, columns, 3)
        plt.imshow(cv2.cvtColor(cam_gb, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Guided XGradCAM")

        print("XGradCAM, Guided backpropagation, and Guided XGradCAM are generated. ")

def xgradcam(model, targetLayer, targetClass, image, dims, device):
    return XGradCAM(model, targetLayer, targetClass, image, dims, device)

class EigenCAM:
    def __init__(self, model, targetLayer, boxes, classes, colors, reshape, image, device):
        self.model = model
        self.targetLayer = targetLayer
        self.boxes = boxes
        self.classes = classes
        self.colors = colors
        self.reshape = reshape
        self.image = image
        self.device = device

    def visualize(self):
        from pytorch_grad_cam import EigenCAM
        from pytorch_grad_cam.utils.image import show_cam_on_image, preprocess_image, scale_cam_image
        import torchvision
        import torch
        import cv2
        import numpy as np
        from PIL import Image
        from IPython.display import display

        self.model.eval().to(self.device)

        rgb_img = np.float32(self.image) / 255
        transform = torchvision.transforms.ToTensor()
        input_tensor = transform(rgb_img)
        input_tensor = input_tensor.unsqueeze(0)
        input_tensor = input_tensor.to(self.device)

        self.targetLayer = [self.targetLayer]

        if self.reshape is None:
            cam = EigenCAM(self.model, self.targetLayer, use_cuda=torch.cuda.is_available())
        else:
            cam = EigenCAM(self.model, self.targetLayer, use_cuda=torch.cuda.is_available(),
                           reshape_transform=self.reshape)
        targets = []
        grayscale_cam = cam(input_tensor=input_tensor, targets=targets, aug_smooth=False,
                            eigen_smooth=False)
        grayscale_cam = grayscale_cam[0, :]
        cam_image = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True)

        renormalized_cam = np.zeros(grayscale_cam.shape, dtype=np.float32)
        for x1, y1, x2, y2 in self.boxes:
            renormalized_cam[y1:y2, x1:x2] = scale_cam_image(grayscale_cam[y1:y2, x1:x2].copy())
        renormalized_cam = scale_cam_image(renormalized_cam)
        eigencam_image_renormalized = show_cam_on_image(rgb_img, renormalized_cam, use_rgb=True)
        for i, box in enumerate(self.boxes):
            color = self.colors[i]
            cv2.rectangle(
                eigencam_image_renormalized,
                (box[0], box[1]),
                (box[2], box[3]),
                color, 2
            )
            cv2.putText(eigencam_image_renormalized, self.classes[i], (box[0], box[1] - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2,
                        lineType=cv2.LINE_AA)

        display(Image.fromarray(np.hstack((cam_image, eigencam_image_renormalized))))

        print("EigenCAM is generated. ")

def eigencam(model, targetLayer, boxes, classes, colors, reshape, image, device):
    return EigenCAM(model, targetLayer, boxes, classes, colors, reshape, image, device)
