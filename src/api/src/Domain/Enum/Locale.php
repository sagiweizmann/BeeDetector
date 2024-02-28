<?php

declare(strict_types=1);

namespace App\Domain\Enum;

use MyCLabs\Enum\Enum;
use TheCodingMachine\GraphQLite\Annotations as GraphQLite;

/**
 * @method static Locale EN()
 * @method static Locale FR()
 */
#[GraphQLite\EnumType]
final class Locale extends Enum
{
    private const EN = 'en';
    private const FR = 'fr';

    private const HE = 'he';

    /**
     * @return string[]
     */
    public static function valuesAsArray(): array
    {
        return [
            self::EN,
            self::FR,
            self::HE,
        ];
    }
}
