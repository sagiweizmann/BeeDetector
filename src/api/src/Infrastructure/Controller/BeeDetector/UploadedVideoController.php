<?php
declare(strict_types=1);

namespace App\Infrastructure\Controller\BeeDetector;

use App\Domain\Model\User;
use App\Infrastructure\Controller\DownloadController;
use App\UseCase\User\GetUser;
use Laminas\Diactoros\Response\JsonResponse;
use Symfony\Component\HttpFoundation\File\Exception\FileException;
use Symfony\Component\HttpFoundation\File\UploadedFile;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;
use TheCodingMachine\GraphQLite\Annotations\Security;

#[Route(path: '/videos')]
final class UploadedVideoController extends DownloadController{

    // upload video
    #[Route(path: '/bee-videos', methods: ['POST'])]
    #[Security("is_granted('IS_AUTHENTICATED_FULLY')")]
    public function uploadVideo(Request $request): JsonResponse
    {
        $uploadedFile = $request->files->get('beeVideo');

        $userId = $request->request->get('userId');

        if (!$uploadedFile instanceof UploadedFile) {
            throw new \InvalidArgumentException('Invalid file uploaded');
        }

        // Generate a unique name for the file before saving it
        $fileName = uniqid().'.'.$uploadedFile->getClientOriginalExtension();
        $target = '';
        $directory = 'bee-videos/' . $userId . '/uploaded-videos/';
        // Move the file to the directory where videos are stored
        try {
            $target = $uploadedFile->move(
                $directory,
                $fileName
            );
        } catch (FileException $e) {
            // Handle the exception
        }
        $target = $directory . $fileName;
        // You may want to do something else with the file, like saving its path to a database
        // return a json response with the target
        return new JsonResponse(['target' => $target]);
        //return new Response('File uploaded successfully' . $fileName .' whhere to ' . $target);
    }
    #[Route(path: '/bee-videos/{filename}', methods: ['GET'])]
    #[Security("is_granted('IS_AUTHENTICATED_FULLY')")]
    public function downloadVideoProfilePicture(
        string $filename
    ): Response {
        return $this->download('bee-videos', $filename);
    }

}